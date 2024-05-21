# from utils import *
# from lowlevel import *
# from midlevel import *
# from general import *

START_BYTE = 0xF0
STOP_BYTE = 0x0F
STUFFING_BYTE = 0x81
STUFFING_KEY = 0x55

def xor_bytes(byte1, byte2):
    return bytes([a ^ b for a, b in zip(byte1, byte2)])


def escape_byte(byte):
    cmd = bytearray()
    if byte == START_BYTE or byte == STOP_BYTE or byte == STUFFING_BYTE:
        cmd += STUFFING_BYTE.to_bytes(1, "big")
        cmd += xor_bytes(byte.to_bytes(1, "big"), STUFFING_KEY.to_bytes(1, "big"))
        return cmd
    cmd += byte.to_bytes(1, "big")
    return cmd


def command_prefix(packet_number, command_number):
    # Make sure the values fit within their respective sizes
    if packet_number < 0 or packet_number > 63:
        raise ValueError("Six-bit value must be between 0 and 63")
    if command_number < 0 or command_number > 1023:
        raise ValueError("Ten-bit value must be between 0 and 1023")

    # Combine the values using bitwise OR and shift operations
    result = (packet_number << 10) | command_number

    # Convert the result to bytes
    bytes_object = result.to_bytes(2, byteorder='big')

    return bytes_object


def strip_header(payload):
    return payload[2:]

def crc_ccitt(data):
    crc = 0x0000
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
    crc &= 0xFFFF
    return crc.to_bytes(2, byteorder='big')


def construct_packet(payload):
    cmd = bytearray()
    cmd += START_BYTE.to_bytes(length=1, byteorder="big")
    packet_length = 1 + 4 + 4 + len(payload) + 1
    packet_length = packet_length.to_bytes(2, byteorder="big")
    # print(len(packet_length))
    # print(cmd.hex())
    for _, val in enumerate(packet_length):
        cmd+=STUFFING_BYTE.to_bytes(length=1, byteorder="big")
        cmd+= xor_bytes(val.to_bytes(1, byteorder="big"), STUFFING_KEY.to_bytes(1, byteorder="big"))
    crc = crc_ccitt(payload)
    for _, val in enumerate(crc):
        cmd+=STUFFING_BYTE.to_bytes(length=1, byteorder="big")
        cmd+= xor_bytes(val.to_bytes(1, byteorder="big"), STUFFING_KEY.to_bytes(1, byteorder="big"))
    for _, val in enumerate(payload):
        cmd+=val.to_bytes(1, byteorder="big")
    cmd.append(STOP_BYTE)
    return cmd

def unstuff_packet(bytes):
    cmd = bytearray()
    prev = False
    for i, val in enumerate(bytes):
        if prev:
            cmd += xor_bytes(bytes[i:i+1], STUFFING_KEY.to_bytes(1, "big"))
        elif val == STUFFING_BYTE:
            prev = True
        else:
            cmd += bytes[i:i+1]
    return cmd

def decode_packet_length(bytes):
    a = xor_bytes(bytes[1:2], STUFFING_KEY.to_bytes(1, "big"))
    b = xor_bytes(bytes[3:4], STUFFING_KEY.to_bytes(1, "big"))
    c = 0
    # print(type(a))
    c |= int.from_bytes(a) << 8
    c |= int.from_bytes(b)
    return c

def decode_packet_checksum(bytes):
    chksum = bytearray()
    a = xor_bytes(bytes[1:2], STUFFING_KEY.to_bytes(1, "big"))
    b = xor_bytes(bytes[3:4], STUFFING_KEY.to_bytes(1, "big"))
    chksum += a
    chksum += b
    return chksum

def decode_message_id(bytes):
    message_id = 0b0000001111111111
    
    message_id &= int.from_bytes(bytes, "big")
    return message_id

def decode_packet_id(bytes):
    packet_id = 0b1111110000000000
    
    packet_id &= int.from_bytes(bytes, "big")

    packet_id = packet_id >> 10
    return packet_id

def receive_packet(serial_device):
    cmd = bytearray()
    print("receiving packet")
    while True:
        a = serial_device.read(1)
        # print("Hello")
        # print(a)
        if a == START_BYTE.to_bytes(1, "big"):
            cmd += a
            # print(a)
            break
    while True:
        a = serial_device.read(1)
        # print(a)
        cmd += a
        if a == STOP_BYTE.to_bytes(1, "big"):
            break
    return cmd



def strip_packet(bytes):
    packet_length = decode_packet_length(bytes[1:5])
    assert packet_length == len(bytes)
    packet_checksum = decode_packet_checksum(bytes[5:9])
    assert packet_checksum == crc_ccitt(bytes[9:packet_length-1])
    message_id = decode_message_id(bytes[9:11])
    packet_id = decode_packet_id(bytes[9:11])

    payload = unstuff_packet(bytes[11:packet_length-1])

    return message_id, packet_id, payload