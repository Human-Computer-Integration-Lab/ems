import serial
import threading
import binascii
import time

get_bin = (
    lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)
)


class Rehastim:
    # We provide a number of ways to initialize an object of class Rehastim

    # It can be passed a serial port. In this case, a SerialHandler will be constructed
    # upon initialization, and the device will use this SerialHandler to communicate

    # It can be passed an already created SerialHandler object. In this case,
    # the provided object will be used to handle all communication.
    # The use case for this is for using a FakeSerialHandler.

    # We initialize an object of class Rehastim by passing it a port.
    # Rationale: We might want to support an arbitrary number of serial
    # devices, and also want to support autodetection of serial devices
    # as a result, we want to separate the detection/choice of serial
    # addresses from the ccreation of the devices.

    # Another difference is that calibration should be handled not in the device,
    # but in the device's handler
    def __init__(self, serial_device):
        # I believe these to be device specific properties
        # Which should therefore be encoded in the device
        # rather than contained in the device's handler
        self.delay = 0.0098  # 9,800 uS
        self.pulseCount = 5
        self.minIntensity = 0
        self.maxIntensity = 32
        self.minPulseWidth = 200
        self.maxPulseWidth = 450
        self.minChannel = 0
        self.maxChannel = 7

        # Open a Serial Port
        # self.ser = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO,
        #                                 #rtscts=True,
        #                                 write_timeout=0,
        #                                 #xonxoff=True,
        #                                 timeout=0)
        self.ser = serial_device

        # Start listening on the serial port
        self.listen = threading.Thread(target=self.__decode_response)
        self.listen.start()

    # A constructor for the class which uses a port
    @classmethod
    def fromPort(cls, port: str):
        s = serial.Serial(
            port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            # rtscts=True,
            write_timeout=0,
            # xonxoff=True,
            timeout=0,
        )
        return cls(s)

    # A constructor which takes in a pre-made serial device
    def fromSerialDevice(cls, dev):
        s = dev
        return cls(s)

    # No longer allow intensity, pulse width to be None
    # This is because calibration data is not stored in this object
    # but is stored in the handler object
    # so it doesn't make sense to fall back on it here - the fall back
    # should occur upstream
    def stim(self, channel: int, intensity: int, pulse_width: int, pulse_count: int):
        # Verify
        if intensity < self.minIntensity:
            raise ValueError(
                "The specified intensity is too low. You provided %d. The minimum intensity is %d"
                % (intensity, self.minIntensity)
            )
        if intensity > self.maxIntensity:
            raise ValueError(
                "The specified intensity is too high. You provided %d. The maximum intensity is %d"
                % (intensity, self.maxIntensity)
            )
        if pulse_width < self.minPulseWidth:
            raise ValueError(
                "The specified pulse width is too low. You provided %d. The minimum pulse width is %d"
                % (pulse_width, self.minPulseWidth)
            )
        if intensity > self.maxIntensity:
            raise ValueError(
                "The specified pulse width is too high. You provided %d. The maximum pulse width is %d"
                % (intensity, self.maxIntensity)
            )
        if channel < self.minChannel:
            raise ValueError("The specified channel is too low")
        if channel > self.maxChannel:
            raise ValueError("The specified channel is too high")

        def stimInThread() -> None:
            for _ in range(pulse_count):
                # if self.calibration[channel][2] <= 0:
                #     continue
                # Generate a single pulse
                # pulse = [self.calibration[channel][0], self.calibration[channel][1], int(self.calibration[channel][2])] # ch, pw, mA
                pulse = [channel, pulse_width, intensity]  # ch, pw, mA
                self.ser.write(self.__generate_pulse(*pulse))
                time.sleep(self.delay)

        self.__runInThread(stimInThread)

    # A method to decode the responses received over the serial port.
    # This can be implemented as just a print statement.
    # However, it could also be extended to provide exceptions,
    # e.g. if the device returns data that is an error
    def __decode_response(self):
        print("Started a listening SerialThread on " + str(self.ser))
        while True:
            v = self.ser.read(size=1)
            if len(v) > 0:
                print("SERIAL_THREAD_RESPONSE:" + str(v))
                # print(v.decode('utf-8'))
                bitstring_v = bin(int.from_bytes(v, byteorder="big"))[2:]
                print(bitstring_v)

    def __generate_pulse(
        self, channel_number: int, pulse_width: int, pulse_current: int
    ):
        # global safety_limit
        ident = 3
        # channel_number = _channel_number-1
        # pulse_width = _pulse_width
        # if (_pulse_current < safety_limit):
        #     pulse_current = _pulse_current
        # else:
        #     print("SAFETY LIMIT (of " + str(safety_limit) + " EXCEEDED. Request of " + str(_pulse_current) + "dropped to limit")
        #     pulse_current = safety_limit
        checksum = (channel_number + pulse_width + pulse_current) % 32
        # print("checksum verify = " + str(checksum))

        # print("binary command: \n" +
        # "\t" + get_bin(ident,2) +  "\t\t#ident\t\t"+ str(len(get_bin(ident,2))) + "\n" +
        # "\t" + get_bin(checksum, 5) + "\t\t#checksum\t" + str(len(get_bin(checksum, 5))) + "\n" +
        # "\t" + get_bin(channel_number,3) + "\t\t#channel_number\t" + str(len(get_bin(channel_number,3))) + "\n" +
        # "\t" + get_bin(pulse_width,9) + "\t#pulse_width\t" + str(len(get_bin(pulse_width,9))) + "\n" +
        # "\t" + get_bin(pulse_current,7) + "\t\t#pulse_current\t" + str(len(get_bin(pulse_current,7))) + "\n"
        # )
        binarized_cmd = (
            get_bin(ident, 2)
            + get_bin(checksum, 5)
            + get_bin(channel_number, 3)
            + get_bin(pulse_width, 9)
            + get_bin(pulse_current, 7)
        )
        cmd_pointer = 0
        new_cmd_pointer = 0
        proper_cmd = ["0" for x in range(32)]

        for c in proper_cmd:
            if new_cmd_pointer == 0:  # add a 1
                proper_cmd[new_cmd_pointer] = "1"
            elif (
                new_cmd_pointer == (9 - 1)
                or new_cmd_pointer == (17 - 1)
                or new_cmd_pointer == (25 - 1)
            ):  # add a 0
                proper_cmd[new_cmd_pointer] = "0"
            elif new_cmd_pointer == (13 - 1) or new_cmd_pointer == (14 - 1):  # add a X
                proper_cmd[new_cmd_pointer] = "0"
            else:
                proper_cmd[new_cmd_pointer] = binarized_cmd[cmd_pointer]
                cmd_pointer += 1
            new_cmd_pointer += 1

        proper_bin_command = "".join(map(str, proper_cmd))
        # print(proper_bin_command)

        hex_command = hex(int(proper_bin_command, 2)).replace("0x", "")
        hex_command = hex_command.replace("L", "")
        print(hex(int(proper_bin_command, 2)))
        return binascii.unhexlify(hex_command)

    def __runInThread(self, f):
        # Create a new thread if currently in the main thread, call f() in this thread otherwise
        if isinstance(threading.current_thread(), threading._MainThread):
            newThread = threading.Thread(target=f)
            newThread.start()
        else:
            f()
