from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from enum import Enum
from typing import Union
import time
import os

GET_LOCK_STATUS_REQ = bytes([91, 2, 148, 0, 150, 0, 93])

class ResponseHashCode(Enum):
    DetailInfo = 1636
    GetLockStatus = 1571
    LockStatusAuto = 1648
    SetUidAndSn1 = 1572

class Command(Enum):
    DetailInfo = 'b7'
    Lock = 'ac'
    SendTinyUidAndSn1 = '95'
    Unlock = 'ad'

class CommandBuilder:
    AEGIS_SESSION_KEY_PADDING = '61622324'
    UNLOCK_COMMAND = 'OpendoorA'
    LOCK_COMMAND = 'CloseDoor'

    def __init__(self, lock_key: bytes, offline_key: bytes, tiny_uid: str):
        self.lock_key = lock_key
        self.offline_key = offline_key
        self.tiny_uid = tiny_uid

    def encrypt(self, data: bytes, aes_key: bytes, aes_iv: bytes, has_padding: bool = True):
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder() if has_padding else None
        if has_padding:
            data = padder.update(data) + padder.finalize()
        return encryptor.update(data) + encryptor.finalize()

    def decrypt(self, encrypted_data: bytes, aes_key: bytes, aes_iv: bytes):
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        return unpadder.update(decrypted_data) + unpadder.finalize()

    def get_session_key(self, encrypt_sn2: bytes, sn1: bytes):
        decrypt_with_iv_hex_str = self.decrypt(encrypt_sn2, self.offline_key, self.lock_key).hex()
        return bytes.fromhex(sn1.hex() + self.AEGIS_SESSION_KEY_PADDING + decrypt_with_iv_hex_str)

    def load_command_with_params(self, cmd: Command, data: Union[str, None] = None):
        head = '5b'
        tail = '5d'

        if data:
            new_str = f'{cmd.value}{self.get_byte_of_data(data)}{data}'
        else:
            new_str = f'{cmd.value}00'

        byte_of_data = self.get_byte_of_data(new_str)
        padded_prefix = self.pad_prefix(hex(self.get_sum_of_data(f'{byte_of_data}{new_str}'))[2:], 2)
        big_small_change = self.get_big_small_change(2, padded_prefix)

        return bytes.fromhex(f'{head}{byte_of_data}{new_str}{big_small_change}{tail}')

    def get_sum_of_data(self, data: str):
        if len(data) < 2:
            return 0
        return int(data[:2], 16) + self.get_sum_of_data(data[2:])

    def pad_prefix(self, data: str, bits: int):
        return data.rjust(bits * 2, '0')

    def get_big_small_change(self, i: int, data: str):
        if not data:
            return ''
        len_data = i * 2
        return f'{data[len_data - 2:len_data]}{data[len_data - 4:len_data - 2]}'

    def get_byte_of_data(self, data: str):
        return self.pad_prefix(hex(len(data) // 2)[2:], 1)

    def get_detail_command(self):
        return self.load_command_with_params(Command.DetailInfo)

    def get_send_tiny_uid_and_sn1_command(self, sn1: bytes):
        new_str = f'FFFF{self.tiny_uid}{self.encrypt(sn1, self.offline_key, self.lock_key).hex()}'
        return self.load_command_with_params(Command.SendTinyUidAndSn1, new_str)

    def get_aegis_local_lock_command(self, sn1: bytes, encrypt_sn2: bytes):
        session_key = self.get_session_key(encrypt_sn2, sn1)
        command_bytes = self.LOCK_COMMAND.encode('utf-8')
        data = self.encrypt(command_bytes, session_key, self.lock_key).hex()
        return self.load_command_with_params(Command.Lock, data)

    def get_aegis_local_unlock_command(self, sn1: bytes, encrypt_sn2: bytes):
        session_key = self.get_session_key(encrypt_sn2, sn1)
        command_bytes = self.UNLOCK_COMMAND.encode('utf-8')
        pad_array = bytes.fromhex('000000')
        secs_hex = format(int(time.time()), 'x')
        padded_prefix = self.pad_prefix(secs_hex, 4)
        time_array = bytes.fromhex(padded_prefix)
        data_buffer = b''.join([command_bytes, pad_array, time_array])
        data = self.encrypt(data_buffer, session_key, self.lock_key, has_padding=False).hex()
        return self.load_command_with_params(Command.Unlock, data)

    def generate_sn1(self):
        return os.urandom(6)
