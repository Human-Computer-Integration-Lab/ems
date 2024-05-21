from ..base import Device
from .PyScienceMode import lowlevel, midlevel, general, utils, decoder
import serial
import time
import threading
import binascii
from typing import List, Tuple

class RehamoveSerial(Device):
    name: str = "RehamoveSerial"

    intensity_min = 0
    intensity_max = 150
    intensity_step = 1

    pulse_width_min = 10
    pulse_width_max = 4000
    pulse_width_step = 1

    n_channels = 8
    delay = 1


    @classmethod
    def from_port(cls, port, **kwargs):
        serial_device = serial.Serial(
            port,
            baudrate=3000000,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            rtscts=True,
            write_timeout=0,
            # xonxoff=True,
            timeout=0,
        )

        lowlevel.LL_init_rt(0, 0, serial_device)
        return cls(serial_device)

    @classmethod
    def guided_setup(cls):
        print("Entering guided setup for the Rehamove device")
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 0:
            raise ValueError("No serial ports available")
        print("Available serial ports:")
        for i, port in enumerate(ports, start=1):
            print(f"{i}. {port.device}")
        while True:
            try:
                choice = int(
                    input("Enter the number of the serial port you want to use: ")
                )
                if choice < 1 or choice > len(ports):
                    print("Invalid choice. Please enter a valid port number.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")
        return cls.from_port(ports[choice - 1].device)

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
            self.pulse(channel, intensity, pulse_width)
            time.sleep(.01)
        # # Verify
        # def stimInThread() -> None:
        #     for _ in range(pulse_count):
        #         # if self.calibration[channel][2] <= 0:
        #         #     continue
        #         # Generate a single pulse
        #         # pulse = [self.calibration[channel][0], self.calibration[channel][1], int(self.calibration[channel][2])] # ch, pw, mA
        #         # self.device.write(self._generate_pulse(channel, pulse_width, intensity))
        #         self.pulse(channel, intensity, pulse_width)
        #         time.sleep(self.delay)

        # self._run_in_thread(stimInThread)

    def _stimulate_in_thread(self, channel, intensity, pulse_width, pulse_count):
        for _ in range(pulse_count):
            self.pulse(channel, intensity, pulse_width)
            time.sleep(self.delay)

    def _decode_response(self):
        """Decodes responses received over the serial port"""
        print("Started a listening SerialThread on " + str(self.ser))
        while True:
            v = self.device.read(size=1)
            if len(v) > 0:
                print("SERIAL_THREAD_RESPONSE:" + str(v))
                # print(v.decode('utf-8'))
                bitstring_v = bin(int.from_bytes(v, byteorder="big"))[2:]
                print(bitstring_v)



    # Direct implementations of basic ScienceMode packets
    # No wrapping or niceties - use if you want the raw output
    # Low Level
    def LL_init(self, voltage: int = 0):
        if voltage <0 or voltage > 6:
            raise ValueError("Incorrect voltage specification. Must be between 0 and 6")
        lowlevel.LL_init_rt(0, voltage, self.device)

    def LL_channel_config(self, channel: int,points: List, stimulation: bool = True):
        if len(points) < 0 or len(points) > 15:
            raise ValueError("Invalid number of points. Must be between 0 and 15")
        lowlevel.LL_channel_config_rt(0, stimulation, channel, points, self.device)

    def LL_stop(self):
        lowlevel.LL_stop_rt(0, self.device)

    # General

    def General_get_version_main(self):
        return general.General_get_version_main_rt(0, self.device)

    def General_get_device_id(self):
        return general.General_Get_device_id_rt(0, self.device)

    def General_get_battery_status(self):
        return general.General_Get_battery_status_rt(0, self.device)
    
    def General_reset(self):
        return general.General_Reset_rt(0, self.device)
    
    def General_get_stim_status_rt(self):
        return general.General_get_stim_status_rt(0, self.device)
    

    # Some wrapped versions of the above functions

    def print_version(self):
        a,b,c,d,e,f = self.General_get_version_main()
        print("FW_Major: %s, FW_Minor: %s, FW_Revision: %s, SMPT_Major: %s, SMPT_Minor: %s, SMPT_Revision: %s"
               % (a,b,c,d,e,f))
        
    def get_fw_major(self):
        a,_, _, _, _, _ = self.General_get_version_main()
        return a
    
    def get_fw_minor(self):
        _,a, _, _, _, _ = self.General_get_version_main()
        return a
    
    def get_fw_rev(self):
        _,_, a, _, _, _ = self.General_get_version_main()
        return a
    
    def get_smpt_major(self):
        _,_, _, a, _, _ = self.General_get_version_main()
        return a
    
    def get_smpt_minor(self):
        _,_, _, _, a, _ = self.General_get_version_main()
        return a
    
    def get_smpt_rev(self):
        _,_, _, _, _, a = self.General_get_version_main()
        return a
        
    def print_device_id(self):
        a = self.General_get_device_id()
        print("Device ID: %s" % a)

    def get_device_id(self):
        return self.General_get_device_id()

    def print_battery_status(self):
        a,b = self.General_get_battery_status()
        print("Level: %d, Voltage: %dmV" %(a,b))

    def get_battery_level_voltage(self):
        a, b = self.General_get_battery_status()
        return a, b
    def get_battery_level(self):
        a, _ = self.General_get_battery_status()
        return a
    
    def get_battery_voltage(self):
        _, a = self.General_get_battery_status()
        return a
    
    def reset(self):
        self.General_reset()


    def pulse(self, channel, current, pulse_width):
        points = []
        points.append((pulse_width, current))
        points.append((pulse_width//2, 0))
        points.append((pulse_width, -current))
        self.LL_channel_config(channel, points, True)

    def _run_in_thread(self, f):
        # Create a new thread if currently in the main thread, call f() in this thread otherwise
        if isinstance(threading.current_thread(), threading._MainThread):
            newThread = threading.Thread(target=f)
            newThread.start()
        else:
            f()

