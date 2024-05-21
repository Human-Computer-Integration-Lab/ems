from .utils import command_prefix, escape_byte, construct_packet, receive_packet, strip_packet

# Encode a get version packet to send from host to device
def General_Get_version_main(packet_id):
    cmd = command_prefix(packet_number=packet_id, 
                         command_number= 50)
    return cmd
# Decode get version packet sent from device to host
def decode_General_Get_version_main_ack(bytes):
    # b0 = bytes[0]
    # if b0==1:
    #     print("Transfer error", b0)
    # else:
    #     print("Firmware Major: ", bytes[1])
    #     print("Firmware Minor: ", bytes[2])
    #     print("Firmware Revision: ", bytes[3])
    #     print("SMPT Major: ", bytes[4])
    #     print("SMPT Minor: ", bytes[5])
    #     print("SMPT Revision: ", bytes[6])
    return bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6]

def General_get_version_main_rt(packet_id, serial_device):
    print("Sending get version")
    packet = construct_packet(General_Get_version_main(packet_id))
    serial_device.write(packet)
    print("Get version: Waiting for response from device")
    response = receive_packet(serial_device)
    message_id, response_packet_id, response_stripped = strip_packet(response)
    if message_id != 51:
        raise ValueError("Failed to complete get version. Error %d" % message_id)
    assert packet_id == response_packet_id
    response_value, firmware_maj, firmware_min,firmware_rev, smpt_maj, smpt_min, smpt_rev = decode_General_Get_version_main_ack(response_stripped)
    if response_value == 1:
        raise RuntimeError("Transfer error in getting version")
    return firmware_maj, firmware_min,firmware_rev, smpt_maj, smpt_min, smpt_rev



# Encode a get device id packet sent from host to device
def General_Get_device_id(packet_id):
    cmd = command_prefix(packet_number=packet_id, 
                         command_number= 52)
    return cmd

# Decode a get device id packet sent from device to host
def decode_General_Get_device_id_ack(bytes):
    # b0 = bytes[0]
    # if b0==1:
    #     print("Transfer error", b0)
    # else:
    #     print(bytes[1:].decode("utf-8"))
    return bytes[0], bytes[1:].decode("utf-8")

def General_Get_device_id_rt(packet_id, serial_device):
    print("Sending get device id")
    packet = construct_packet(General_Get_device_id(packet_id))
    serial_device.write(packet)
    print("Get device id: Waiting for response from device")
    response = receive_packet(serial_device)
    message_id, response_packet_id, response_stripped = strip_packet(response)
    if message_id != 53:
        raise ValueError("Failed to complete get device id. Error %d" % message_id)
    assert packet_id == response_packet_id
    response_value, device_id = decode_General_Get_device_id_ack(response_stripped)
    if response_value == 1:
        raise RuntimeError("Transfer error in getting device id")
    return device_id


# Encode a battery status packet to send to device
def General_Get_battery_status(packet_id):
    cmd = command_prefix(packet_number=packet_id, 
                         command_number= 54)
    return cmd

# Decode a battery status packet sent to device (for reverse engineering)
def decode_General_Get_battery_status(payload):
    print("Host requested battery status")

# Encode a battery status ack sent from device to host (for reverse engineering)
def General_Get_battery_status_ack(packet_id, error, level, voltage):
    cmd = command_prefix(packet_id, 55)

    b = 0
    if error:
        b |= 0b1
    cmd+=b.to_bytes(1, "big")
    

    cmd += level.to_bytes(1, "big")
    cmd += voltage.to_bytes(2, "big")
    return cmd
    
# Decode a battery status ack sent from device to host
def decode_General_Get_battery_status_ack(bytes):
    b0 = bytes[0]
    return bytes[0], bytes[1], int.from_bytes(bytes[2:4])

def General_Get_battery_status_rt(packet_id, serial_device):
    print("Sending Get battery status")
    packet = construct_packet(General_Get_battery_status(packet_id))
    serial_device.write(packet)
    print("Get battery status: Waiting for response from device")
    response = receive_packet(serial_device)
    message_id, response_packet_id, response_stripped = strip_packet(response)
    if message_id != 55:
        raise ValueError("Failed to complete get battery status. Error %d" % message_id)
    assert packet_id == response_packet_id
    response_value, voltage, current = decode_General_Get_battery_status_ack(response_stripped)
    if response_value == 1:
        raise RuntimeError("Transfer error in getting battery status")
    return voltage, current



# Encode a reset packet to the device
def General_Reset(packet_id):
    cmd = command_prefix(packet_number=packet_id, 
                         command_number= 58)
    return cmd

def General_Reset_rt(packet_id, serial_device):
    print("Sending Reset Command")
    packet = construct_packet(General_Get_battery_status(packet_id))
    serial_device.write(packet)
    response = receive_packet(serial_device)


# Encode a get stim status packet to send from host to device
def General_Get_stim_status(packet_id):
    cmd = command_prefix(packet_number=packet_id, 
                         command_number= 62)
    return cmd

# Decode a get stim status packet sent from device to host
def decode_General_Get_stim_status_ack(bytes):
    # b0 = bytes[0]
    # if b0==1:
    #     print("Transfer error", b0)
    # else:
    #     print("Stim-status", bytes[1])
    #     print("High voltage level", bytes[2])
    return bytes[0], bytes[1], bytes[2]

def General_get_stim_status_rt(packet_id, serial_device):
    print("Sending Get stim status")
    packet = construct_packet(General_Get_stim_status(packet_id))
    serial_device.write(packet)
    print("Get stim status: Waiting for response from device")
    response = receive_packet(serial_device)
    message_id, response_packet_id, response_stripped = strip_packet(response)
    if message_id != 63:
        raise ValueError("Failed to complete get stim status. Error %d" % message_id)
    assert packet_id == response_packet_id
    response_value, status, voltage_level = decode_General_Get_battery_status_ack(response_stripped)
    if response_value == 1:
        raise RuntimeError("Transfer error in getting stim status")
    return status, voltage_level

def General_Get_extended_version(packet_id):
    cmd = command_prefix(packet_number=packet_id,
                         command_number=68)
    return cmd


def decode_General_error(bytes):
    print("Error value: ", bytes[0])
# # Only for science mode 4 I think
# def decode_General_Get_extended_version_ack(bytes):
#     b0 = bytes[0]
#     if b0==1:
#         print("Transfer error", b0)
#     else:
#         print("Firmware Major: ", bytes[1])
#         print("Firmware Minor: ", bytes[2])
#         print("Firmware Revision: ", bytes[3])
#         print("SMPT Major: ", bytes[4])
#         print("SMPT Minor: ", bytes[5])
#         print("SMPT Revision: ", bytes[6])



# def decode_General_Get_battery_status_ack(bytes):
#     b0 = bytes[0]
#     if b0==1:
#         print("Transfer error", b0)
#     else:
#         print("Battery level", bytes[1])
#         print("Battery voltage", int.from_bytes(bytes[2:3]))


# def decode_General_Get_stim_status_ack(bytes):
#     # b0 = bytes[0]
#     # if b0==1:
#     #     print("Transfer error", b0)
#     # else:
#     #     print("Stim-status", bytes[1])
#     #     print("High voltage level", bytes[2])
#     return bytes[0], bytes[1], bytes[2]




