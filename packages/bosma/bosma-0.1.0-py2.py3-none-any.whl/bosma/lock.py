import asyncio
import sys
from enum import Enum
from typing import Union

from collections.abc import Callable
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection

from .model import LockState, Connectivity
from .command import GET_LOCK_STATUS_REQ, CommandBuilder, ResponseHashCode
from .parsers import (
    parse_get_lock_status_resp,
    parse_lock_status_auto_resp,
    parse_set_uid_and_sn1_resp,
    return_payload_to_hash_code,
)
import logging

_LOGGER = logging.getLogger(__name__)


WRITE_CHAR = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
NOTIFY_CHAR = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
LOCK_KEY_IV = bytes("5beba2290a7fc515", "utf-8")
KEEP_ALIVE_TIMEOUT = 30


class LockOperation(Enum):
    UNLOCK = "unlock"
    LOCK = "lock"


class AegisLock:
    def __init__(self, offline_key: bytes, tiny_uid: str) -> None:
        self._lock_key = LOCK_KEY_IV
        self._offline_key = offline_key
        self._update_task: asyncio.Task[None] | None = None
        self._tiny_uid = tiny_uid
        self._command_builder = CommandBuilder(self._lock_key, offline_key, tiny_uid)
        self._pending_cmd: Union[LockOperation, None] = None
        self._pending_sn1: Union[bytes, None] = None
        self._loop = asyncio._get_running_loop()
        self._keep_alive_timer: asyncio.TimerHandle | None = None
        self._device: BLEDevice | None = None
        self._client: BleakClient | None = None
        self.state: LockState | None = None
        self._callbacks: list[Callable[[LockState, Connectivity], None]] = []
        self._enable_keep_alive = False

    async def connect(self, device: BLEDevice, keep_alive=True):
        self._enable_keep_alive = keep_alive

        def _disconnect_callback(client: BleakClient):
            _LOGGER.debug(f"{device.address} has disconnected")
            self._update_state(self.state)

        _LOGGER.debug(f"connecting to device @ {device.address}")
        self._client = await establish_connection(
            BleakClient,
            device,
            device.address,
            disconnected_callback=_disconnect_callback,
        )
        self._device = device
        _LOGGER.debug(f"connected!")
        await self._client.start_notify(NOTIFY_CHAR, self._notification_cb)

        if keep_alive:
            self._schedule_update()
            self._schedule_keep_alive()
        else:
            await self.update()

    def register_callback(self, callback: Callable[[LockState, Connectivity], None]):
        _LOGGER.debug(f"registering callback")

        def unregister_callback() -> None:
            self._callbacks.remove(callback)

        self._callbacks.append(callback)
        return unregister_callback

    def _update_state(self, new_state: LockState):
        _LOGGER.debug(f"updating state")
        self.state = new_state
        if not self._callbacks:
            return

        for callback in self._callbacks:
            try:
                connectivity = (
                    Connectivity.CONNECTED
                    if self.is_connected()
                    else Connectivity.DISCONNECTED
                )
                callback(new_state, connectivity)
            except Exception as ex:  # pylint: disable=broad-except
                # log or something?
                _LOGGER.error("Error while updating state")
                _LOGGER.error(ex)
                return

    async def _notification_cb(self, _: BleakGATTCharacteristic, data: bytes):
        hex_data = data.hex()
        hash_code = return_payload_to_hash_code(hex_data)
        _LOGGER.debug(f"incoming notification")

        if hash_code == ResponseHashCode.GetLockStatus.value:
            _LOGGER.debug(f"GetLockStatus")
            self._update_state(parse_get_lock_status_resp(hex_data))

        if hash_code == ResponseHashCode.LockStatusAuto.value:
            _LOGGER.debug(f"LockStatusAuto")
            self._update_state(parse_lock_status_auto_resp(hex_data))

        if hash_code == ResponseHashCode.SetUidAndSn1.value:
            _LOGGER.debug(f"SetUidAndSn1")
            sn2 = parse_set_uid_and_sn1_resp(hex_data)
            data = b""
            cmd = (
                self._command_builder.get_aegis_local_lock_command
                if self._pending_cmd == LockOperation.LOCK
                else self._command_builder.get_aegis_local_unlock_command
            )

            data = cmd(self._pending_sn1, sn2)
            await self._client_write(data)

    async def _client_write(self, data: bytes):
        _LOGGER.debug(f"writing data to GATT")

        # Reschedule keep alive if this isn't the update task
        if self._update_task and self._update_task.done():
            self._reschedule_keep_alive()

        await self._ensure_connection()
        return await self._client.write_gatt_char(WRITE_CHAR, data, response=True)

    async def _lock_unlock(self, pending_cmd: LockOperation):
        self._pending_cmd = pending_cmd
        self._pending_sn1 = self._command_builder.generate_sn1()
        await self._client_write(
            self._command_builder.get_send_tiny_uid_and_sn1_command(self._pending_sn1)
        )

    async def lock(self):
        _LOGGER.debug(f"Locking")
        await self._lock_unlock(LockOperation.LOCK)

    async def unlock(self):
        _LOGGER.debug(f"Unlocking")
        await self._lock_unlock(LockOperation.UNLOCK)

    async def disconnect(self):
        _LOGGER.debug(f"Disconnecting device")
        self._cancel_keepalive_timer()
        await self._client.stop_notify(NOTIFY_CHAR)
        await self._client.disconnect()
        self._client = None

    def _cancel_keepalive_timer(self) -> None:
        if self._keep_alive_timer:
            self._keep_alive_timer.cancel()
            self._keep_alive_timer = None

    async def _ensure_connection(self):
        if not self._client:
            _LOGGER.error("No client available")
        if not self._client.is_connected and self._device:
            _LOGGER.debug("disconnected. attempting reconnect")
            await self.connect(self._device, self._enable_keep_alive)

    def _reschedule_keep_alive(self):
        _LOGGER.debug("rescheduling keep alive")
        self._cancel_keepalive_timer()
        self._schedule_keep_alive()

    def _schedule_update(self):
        _LOGGER.debug("scheduling next update")
        self._update_task = asyncio.create_task(self._update_data())
        _LOGGER.debug("next update scheduled")

    def _schedule_keep_alive(self):
        _LOGGER.debug("scheduling next keep alive")
        self._keep_alive_timer = self._loop.call_later(
            KEEP_ALIVE_TIMEOUT, self._run_keep_alive
        )

    def _run_keep_alive(self):
        asyncio.create_task(self._keep_alive())

    async def _keep_alive(self):
        if not self._enable_keep_alive:
            return

        _LOGGER.debug("keep alive running")

        await self._ensure_connection()
        await self.update()
        self._schedule_keep_alive()

    async def update(self):
        await self._update_data()

    async def _update_data(self):
        _LOGGER.debug("_update_data")
        await self._client_write(GET_LOCK_STATUS_REQ)

    def address(self):
        return self._device.address

    def is_connected(self):
        return self._client.is_connected
