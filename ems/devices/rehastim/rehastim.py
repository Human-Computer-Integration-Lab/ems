from ..base import Device

import serial
import time
import threading
import binascii


class Rehastim(Device):
    name: str = "rehastim"

    # Current [0, 2, ..., 126] mA in 2 mA steps
    intensity_conf = set(list(range(0, 126 + 2, 2)))

    # Pulsewidth [0, 20, 21, ..., 500] µs in 1 µs steps
    pulse_conf = set(list(range(20, 500 + 1, 1))).add(0)

    # Channels 8 (2 times 4 on two modules)
    n_channels = 8

    @classmethod
    def from_port(cls, port, **kwargs):
        serial_device = serial.Serial(
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
        return cls(serial_device)

    def stimulate(
        self,
        channel: int,
        intensity: int,
        pulse_width: int,
        pulse_count: int,
        validate_params: bool = True,
    ):
        if validate_params:
            self.validate(channel, intensity, pulse_width)

        # Verify
        def stimInThread() -> None:
            for _ in range(pulse_count):
                # if self.calibration[channel][2] <= 0:
                #     continue
                # Generate a single pulse
                # pulse = [self.calibration[channel][0], self.calibration[channel][1], int(self.calibration[channel][2])] # ch, pw, mA
                self.ser.write(self._generate_pulse(channel, pulse_width, intensity))
                time.sleep(self.delay)

        self._runInThread(stimInThread)

    def _stimulate_in_thread(self, channel, intensity, pulse_width, pulse_count):
        for _ in range(pulse_count):
            self.ser.write(self._generate_pulse(channel, pulse_width, intensity))
            time.sleep(self.delay)

    def _decode_response(self):
        """Decodes responses received over the serial port"""
        print("Started a listening SerialThread on " + str(self.ser))
        while True:
            v = self.ser.read(size=1)
            if len(v) > 0:
                print("SERIAL_THREAD_RESPONSE:" + str(v))
                # print(v.decode('utf-8'))
                bitstring_v = bin(int.from_bytes(v, byteorder="big"))[2:]
                print(bitstring_v)

    def _generate_pulse(
        self, channel_number: int, pulse_width: int, pulse_current: int
    ):
        ident = 3
        checksum = (channel_number + pulse_width + pulse_current) % 32

        get_bin = (
            lambda x, n: x >= 0
            and str(bin(x))[2:].zfill(n)
            or "-" + str(bin(x))[3:].zfill(n)
        )

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

    def _run_in_thread(self, f):
        # Create a new thread if currently in the main thread, call f() in this thread otherwise
        if isinstance(threading.current_thread(), threading._MainThread):
            newThread = threading.Thread(target=f)
            newThread.start()
        else:
            f()
