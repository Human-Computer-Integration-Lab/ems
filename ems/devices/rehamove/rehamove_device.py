from ..base import Device
import serial.tools.list_ports
from . import rehamove


class Rehamove(Device):
    name: str = "rehamove"
    # TODO: fix this
    intensity_min = 0
    intensity_max = 126
    intensity_step = 2

    pulse_width_min = 20
    pulse_width_max = 500
    pulse_width_step = 1

    n_channels = 8
    @classmethod
    def from_port(cls, port, **kwargs):
        d = rehamove.Rehamove(port)
        return cls(d)
    
    @classmethod
    def guided_setup(cls):
        print("Entering guided setup for the Rehastim device")
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 0:
            raise ValueError("No serial ports available")
        print("Available serial ports:")
        for i, port in enumerate(ports, start=1):
            print(f"{i}. {port.device}")
        while True:
            try:
                choice = int(input("Enter the number of the serial port you want to use: "))
                if choice < 1 or choice > len(ports):
                    print("Invalid choice. Please enter a valid port number.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")
        return cls.from_port(ports[choice-1].device)

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
        for _ in range(pulse_count):
            self.device.pulse(channel, intensity, pulse_width)