import binascii
from .model import LockedStatus, DoorStatus, LockState

def get_substring(s, start, end):
    return s[start:end]

def parse_int_hex(s):
    return int(s, 16)

def parse_get_lock_status_resp(hex_str):
    lock_status = LockedStatus.LOCK if parse_int_hex(get_substring(hex_str, 8, 10)) == 1 else LockedStatus.UNLOCK
    battery = min(max(0, parse_int_hex(get_substring(hex_str, 10, 12))), 100)
    z = parse_int_hex(get_substring(hex_str, 12, 14)) == 1
    door_status = DoorStatus.CLOSED if  parse_int_hex(get_substring(hex_str, 14, 16)) == 1 else DoorStatus.OPEN

    # return {"battery": battery, "doorStatus": door_status, "lockStatus": lock_status}
    return LockState(battery, door_status, lock_status)

def parse_lock_status_auto_resp(hex_str):
    lock_status = LockedStatus.LOCK if parse_int_hex(get_substring(hex_str, 8, 10)) == 1 else LockedStatus.UNLOCK
    door_status = DoorStatus.CLOSED if parse_int_hex(get_substring(hex_str, 10, 12)) == 1 else DoorStatus.OPEN
    battery = parse_int_hex(get_substring(hex_str, 12, 14))
    # unlock_type = parse_int_hex(get_substring(hex_str, 14, 16))

    # return {"battery": battery, "doorStatus": door_status, "lockStatus": lock_status, "UnlockType": unlock_type}
    return LockState(battery, door_status, lock_status)

def hash_code(s):
    h = 0
    for i in range(len(s)):
        h = (31 * h + ord(s[i])) & 0xFFFFFFFF  # Ensure it's a 32-bit integer
    return h

def return_payload_to_hash_code(s):
    return hash_code(s[4:6])

def parse_set_uid_and_sn1_resp(hex_str):
    sn2_hex = hex_str[8:40]
    sn2_bytes = binascii.unhexlify(sn2_hex)
    return sn2_bytes


def parse_get_aegis_detail_resp(hex_str):
    lock_status = parse_int_hex(hex_str[34:36])
    door_status = parse_int_hex(hex_str[36:38])
    timeout_value = hex_str[62:66]

    return {"doorStatus": door_status, "lockStatus": lock_status, "timeoutValue": timeout_value}
