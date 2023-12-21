from enum import Enum
from dataclasses import dataclass


class LockedStatus(Enum):
    UNLOCK = 0
    LOCK = 1


class DoorStatus(Enum):
    CLOSED = 0
    OPEN = 1


@dataclass
class LockState:
    battery: int
    door: DoorStatus
    lock: LockedStatus


class Connectivity(Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
