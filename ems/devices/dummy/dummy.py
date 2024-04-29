from ..base import Device

import serial
import serial.tools.list_ports
import time
import threading
import binascii


class Dummy(Device):
    name: str = "Dummy Device"
    pulse_count: int = 5
    min_intensity: int = 0
    max_intensity: int = 32
    min_pulse_width: int = 200
    max_pulse_width: int = 450
    min_channel: int = 0
    max_channel: int = 7

    def __repr__(self):
        # used to display device-specific information (name, make, model, battery, etc.)
        print("I'm a dummy device")
        pass


    @classmethod
    def from_port(cls, port, **kwargs):
        return cls(None)
    
    # A constructor which takes in a pre-made serial device
    @classmethod
    def from_serial_device(cls, dev):
         return cls(dev)

    @classmethod
    def guided_setup(cls):
        print("The dummy device requires no guided setup")
        print("Let's still fake the serial port selection")

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
        return cls(None)

    # No longer allow intensity, pulse width to be None
    # This is because calibration data is not stored in this object
    # but is stored in the handler object
    # so it doesn't make sense to fall back on it here - the fall back 
    # should occur upstream
    def stimulate(self, channel : int, intensity : int, pulse_width: int, pulse_count : int):
        print("I'm stimulating!")
        print("Dummy Device: Stimulating channel %d with intensity %d, pulse width %d, pulse count %d" % (channel, intensity, pulse_width, pulse_count))




