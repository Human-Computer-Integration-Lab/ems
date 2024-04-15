from .base import Device

import serial


class Rehastim(Device):
    name: str = "rehastim"
    pulse_count: int = 5
    min_intensity: int = 0
    max_intensity: int = 32
    min_pulse_width: int = 200
    max_pulse_width: int = 450
    min_channel: int = 0
    max_channel: int = 7

    def __repr__(self):
        # used to display device-specific information (name, make, model, battery, etc.)
        pass

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

    def stimulate(self):
        pass
