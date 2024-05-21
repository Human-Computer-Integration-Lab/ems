from .lowlevel import *
from .midlevel import *
from .general import *
from .utils import *

decode_dict = {
    0  : decode_LL_init,
    1  : decode_LL_init_ack,
    2  : decode_LL_Channel_Config,
    3  : decode_LL_channel_config_ack,
    4  : decode_LL_stop, 
    5  : decode_LL_stop_ack,
    30 : decode_ML_Init,
    51 : decode_General_Get_version_main_ack,
    53 : decode_General_Get_device_id_ack, 
    54 : decode_General_Get_battery_status,
    55 : decode_General_Get_battery_status_ack,
    63 : decode_General_Get_stim_status_ack,
    # 69 : decode_General_Get_extended_version_ack
}



def decode_packet(bytes):
    packet_length = decode_packet_length(bytes[1:5])
    assert packet_length == len(bytes)
    packet_checksum = decode_packet_checksum(bytes[5:9])
    assert packet_checksum == crc_ccitt(bytes[9:packet_length-1])
    message_id = decode_message_id(bytes[9:11])
    packet_id = decode_packet_id(bytes[9:11])

    payload = unstuff_packet(bytes[11:packet_length-1])

    decode_dict[message_id](payload)
    # if message_id == 3:
    #     decode_LL_channel_config_ack(payload)
    # elif message_id == 5:
    #     decode_LL_stop_ack(payload)
    # elif message_id == 51:
    #     decode_Get_version_main_ack(payload)
    # elif message_id == 53:
    #     decode_Get_device_id_ack(payload)
    # elif message_id == 55:
    #     decode_Get_battery_status_ack(payload)
    # elif message_id == 63:
    #     decode_Get_stim_status_ack(payload)
    # elif message_id == 69:
    #     decode_Get_extended_version_ack(payload)
    
    print("Message id:", message_id)
    print("Packet id", packet_id)


def respond_packet(bytes):
    packet_length = decode_packet_length(bytes[1:5])
    assert packet_length == len(bytes)
    packet_checksum = decode_packet_checksum(bytes[5:9])
    assert packet_checksum == crc_ccitt(bytes[9:packet_length-1])
    message_id = decode_message_id(bytes[9:11])
    packet_id = decode_packet_id(bytes[9:11])

    payload = unstuff_packet(bytes[11:packet_length-1])

    # decode_dict[message_id](payload)

    if message_id == 54:
        return construct_packet(General_Get_battery_status_ack(packet_id, 0, 30, 24000))
    if message_id == 2:
        return construct_packet(LL_channel_config_ack(packet_id, 0, 0))
    if message_id == 4:
        return construct_packet(LL_stop_ack(packet_id, 0))
    if message_id == 30:
        return construct_packet(ML_init_ack(packet_id, 0))
    # if message_id == 3:
    #     decode_LL_channel_config_ack(payload)
    # elif message_id == 5:
    #     decode_LL_stop_ack(payload)
    # elif message_id == 51:
    #     decode_Get_version_main_ack(payload)
    # elif message_id == 53:
    #     decode_Get_device_id_ack(payload)
    # elif message_id == 55:
    #     decode_Get_battery_status_ack(payload)
    # elif message_id == 63:
    #     decode_Get_stim_status_ack(payload)
    # elif message_id == 69:
    #     decode_Get_extended_version_ack(payload)
    
    print("Message id:", message_id)
    print("Packet id", packet_id)