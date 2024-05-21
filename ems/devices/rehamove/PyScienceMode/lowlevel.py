from .utils import command_prefix, escape_byte, receive_packet,construct_packet, strip_packet
# from decoder import decode_packet

# Encode a packet to send from host to device
def LL_Init(packet_id, voltage):
    cmd=  command_prefix(packet_number = packet_id, 
                          command_number=0)
    def create_byte(number):
        # Ensure number is in the range [0, 6]
        number = max(0, min(6, number))
        
        # First 4 bits are 0
        byte = 0
        
        # Set the next 3 bits with the provided number
        byte |= (number & 0b111) << 1
        
        # Last bit is 0
        byte &= 0b11111110
        
        return byte.to_bytes(1, "big")
    
    cmd += create_byte(voltage)
    return cmd


# Decode a packet sent from host to device (for reverse engineering)
def decode_LL_init(payload):
    voltages = ["Standard (150v)", 
                "OFF", 
                "30v", 
                "60v",
                "90v", 
                "120v", 
                "150v"]

    def decode_byte(byte):
        # Convert the byte to an integer
        byte_int = int.from_bytes(byte, "big")
        
        # Extract the bits that represent the number
        # The number is in bits 1, 2, and 3 (second, third, and fourth bits from the right)
        number = (byte_int >> 1) & 0b111
        
        return number
    print("Voltage setting: ", voltages[decode_byte(payload)])

# Encode a packet sent from device to host (for reverse engineering)
def LL_init_ack(packet_id, status):
    cmd = command_prefix(packet_number = packet_id, 
                          command_number=1)

    cmd += status.to_bytes(1, "big")
    return cmd

# Decode a packet sent from device to host
def decode_LL_init_ack(payload):
    b1 = payload[0]
    return b1


# Construct, send, receive ack for Low-Level initialization
def LL_init_rt(packet_id, voltage, serial_device):
    print("Initiating low level stimulation mode")
    packet = construct_packet(LL_Init(packet_id, voltage))
    # print(packet.hex())
    serial_device.write(packet)
    print("Initiate LL: Waiting for response from device")
    response = receive_packet(serial_device)
    message_id, response_packet_id, response_stripped = strip_packet(response)
    if message_id != 1:
        raise ValueError("Failed to initialize low-level mode. Error %d" % message_id)
    assert packet_id == response_packet_id
    response_value = decode_LL_init_ack(response_stripped)
    if response_value == 1:
        raise RuntimeError("Transfer error in initiating low-level mode")
    if response_value == 2:
        raise ValueError("Parameter error in initiating low-level mode")
    if response_value == 4:
        raise RuntimeError("Timeout error in initiating low-level mode")
    else:
        print("Successfully initialized low level mode")

# Encode a packet to send from host to device
def LL_Channel_Config(packet_id, stimulate, channel, points):
    cmd=  command_prefix(packet_number = packet_id, 
                            command_number=2)
    channel = max(0, min(3, channel))
    
    byte = 0
    
    if stimulate:
        byte |= 0b10000000
    byte |= (channel & 0b11) << 5
    
    # Set the fifth bit with the provided value
    byte |= len(points)-1 & 0b1111
    # print("mybyte", byte.to_bytes(1, "big").hex())
    cmd += byte.to_bytes(1, "big")
    for (x, y) in points:
        cmd += LL_Point(x, y).to_bytes(4, "big")

    # stuffed = bytearray()
    # for _, val in enumerate(cmd):
    #     stuffed += escape_byte(val)
    # return stuffed
    return cmd


# Decode a packet sent from host to device (for reverse engineering)
def decode_LL_Channel_Config(packet):
    byte = packet[0]
    
    # Extract stimulate flag
    stimulate = bool(byte & 0b10000000)
    
    # Extract channel
    channel = (byte >> 5) & 0b11
    
    # Extract number of points
    num_points = (byte & 0b1111) + 1
    
    points = []
    for i in range(num_points):
        point_data = packet[1 + i * 4 : 1 + (i + 1) * 4]
        encoded_point = int.from_bytes(point_data, 'big')
        duration, current = decode_LL_Point(encoded_point)
        points.append((duration, current))
    
    # return {
    #     "stimulate": stimulate,
    #     "channel": channel,
    #     "points": points
    # }
    print("Stimulate: ", stimulate)
    print("Channel: ", channel)
    print("Num Points", num_points)
    print("Points:", points)
    # print("Channel": channel)

# Encode a response packet sent from device to host (for reverse engineering)
def LL_channel_config_ack(packet_id, result, error_channel):
    cmd = command_prefix(packet_id, 3)

    cmd += result.to_bytes(1, "big")
    if result == 10:
        cmd += error_channel.to_bytes(1, "big")
    else:
        x = 0
        cmd += x.to_bytes(1, "big")
    return cmd


# Decode a response packet sent from device to host
def decode_LL_channel_config_ack(bytes):
    b1 = bytes[0]
    b2 = bytes[1]
    return b1, b2


# Construct, send, receive a packet for channel config
def LL_channel_config_rt(packet_id, stimulate, channel, points, serial_device):
    print("Sending Low Level Channel Config")
    packet = construct_packet(LL_Channel_Config(packet_id, stimulate, channel, points))
    serial_device.write(packet)
    print("LL Channel Config: Waiting for response from device")
    response = receive_packet(serial_device)
    message_id, response_packet_id, response_stripped = strip_packet(response)
    if message_id != 3:
        raise ValueError("Failed to initialize low-level mode. Error %d" % message_id)
    assert packet_id == response_packet_id
    response_value, error_channel = decode_LL_channel_config_ack(response_stripped)
    if response_value == 1:
        raise RuntimeError("Transfer error in initiating low-level mode")
    if response_value == 2:
        raise ValueError("Parameter error in initiating low-level mode")
    if response_value == 4:
        raise RuntimeError("Timeout error in initiating low-level mode")
    if response_value == 7:
        raise RuntimeError("Stimulation not initialized")
    if response_value == 10:
        raise RuntimeError("Electrode %d error" % error_channel)
    else:
        print("Successfully sent LL Channel Config")




# Encode a point subpacket to be sent from host to device
def LL_Point(duration, current):
    b = 0

    b |= (duration & 0b111111111111) << 20
    b |= (300 + 2*(current) & 0b1111111111) << 10
    # print("Encoded: ", (300 + 2*(current) & 0b1111111111))
    return b
# Encode a point subpacket sent from host to device (for reverse engineering)
def decode_LL_Point(encoded_point):
    # Extract duration
    duration = (encoded_point >> 20) & 0b111111111111
    # Extract current
    # current = ((encoded_point >> 10) & 0b1111111111)
    # print(current)
    current = (((encoded_point >> 10) & 0b1111111111) - 300) // 2
    # current -= 300
    # current //=2
    return duration, current


# Encode a LL_Stop packet to send from host to device
def LL_Stop(packet_id):
    return command_prefix(packet_number = packet_id, 
                          command_number=4)

# Decode an LL_Stop packet sent from host to device (for reverse engineering)
def decode_LL_stop(payload):
    def decode_byte(byte):
        # Convert the byte to an integer
        byte_int = int.from_bytes(byte, "big")
        
        # Extract the bits that represent the number
        # The number is in bits 1, 2, and 3 (second, third, and fourth bits from the right)
        number = (byte_int >> 1) & 0b111
        
        return number
    print("LL Stop returned: ", decode_byte(payload))

# Encode an LL_Stop packet sent from device to host (for reverse engineering)
def LL_stop_ack(packet_id, result):
    cmd = command_prefix(packet_id, 5)
    cmd += result.to_bytes(1, "big")
    return cmd

# Decode an LL_Stop ack packet sent from device to host
def decode_LL_stop_ack(bytes):
    b1 = bytes[0]
    return b1


# Construct, send, receive a packet for channel config
def LL_stop_rt(packet_id, serial_device):
    print("Sending Low Level Stop")
    packet = construct_packet(LL_Stop(packet_id))
    serial_device.write(packet)
    print("Stop LL: Waiting for response from device")
    response = receive_packet(serial_device)
    message_id, response_packet_id, response_stripped = strip_packet(response)
    if message_id != 5:
        raise ValueError("Failed to initialize low-level mode. Error %d" % message_id)
    assert packet_id == response_packet_id
    response_value = decode_LL_stop_ack(response_stripped)
    if response_value == 1:
        raise RuntimeError("Transfer error in stopping low-level mode")
    else:
        print("Successfully stopped LL Mode")
