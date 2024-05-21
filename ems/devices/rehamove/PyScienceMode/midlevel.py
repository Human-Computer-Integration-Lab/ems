from .utils import command_prefix, escape_byte



def ML_Init(packet_id):
    cmd = command_prefix(packet_number=packet_id, 
                         command_number= 30)
    byte = 0
    cmd += byte.to_bytes(1, "big")
    return cmd


def ML_init_ack(packet_id, status):
    cmd=  command_prefix(packet_number = packet_id, 
                          command_number=31)

    cmd += status.to_bytes(1, "big")
    return cmd

def decode_ML_Init(payload):
    print("Mid level initiated")

# def ML_Update(packet_id, c1, c2, c3, c4, c1pts, c2pts, c3pts, c4pts, c1period, c2period, c3period, c4period):
#     cmd = command_prefix(packet_number=packet_id, 
#                          command_number= 32)
#     byte = 0
#     if c1:
#         byte |= 0b10000000
#     if c2:
#         byte |= 0b01000000
#     if c3:
#         byte |= 0b00100000
#     if c3:
#         byte |= 0b00010000
#     cmd += byte.to_bytes(1, "big")
#     return cmd
def ML_Get_current_data(packet_id):
    cmd = command_prefix(packet_number=packet_id, 
                         command_number= 36)
    byte = 2
    cmd += byte.to_bytes(1, "big")
    return cmd

# F0 81558158 81168194 082402 0F
# f0 81558158 81168194 082402 0f
def ML_Stop(packet_id):
    cmd = command_prefix(packet_number=packet_id, 
                         command_number= 34)
    return cmd