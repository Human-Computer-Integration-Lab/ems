from serial.tools import list_ports
from collections import defaultdict
import time
class Device:
    # Baseline initiate function which just takes 
    def __init__(self, stimulator_handle):
        self.dev = stimulator_handle
        self.calibration = {}
        self.channel_calibrated = defaultdict(lambda: False)


    @classmethod
    def fromAutoDetect():
        # List devices
        ports = list(list_ports.comports())
        print(f"Serial ports: {ports}")
        # ask user to choose device
        # some kind of flow to select the right kind of device to
        # create
        # Then call the std init function. 

    def load_calibration_file():
        #TODO
        return

    def write_calibration_file():
        #TODO
        return
    def calibrate(self, channel, pulse_width = 300, pulse_count = 40):

        # ems = SerialThingy.SerialThingy(FAKE_SERIAL)
        # if len(sys.argv) > 1:
        #         ems.open_port(str(sys.argv[1]),serial_response_active) # pass the port via the command line, as an argument
        # else:
        #         ems.open_port(serial_response_active)

        while 1:
            print("current intensity (0-100mA, limited 32mA): ")
            print(intensity)
            user_input = input('set intensity (enter to repeat current one, done to finish): ')
            if user_input == "done":
                print("calibration done")
                print("intensity for you: ")
                print(intensity)
                self.calibration[channel] = intensity
                self.channel_calibrated[channel] = True
                break
            elif user_input != "":
                intensity = int(user_input)
            self.dev.stim(channel, intensity, pulse_width, pulse_count)
            # for i in range(pulse_count):
            #     ems.write(singlepulse.generate(channel, pulse_width, intensity))
            #     #ems.write(singlepulse.generate(channel+1, pulse_width, intensity-5))
            #     #channel number (1-8), pulse width (200-450) in microseconds, intensity (0-100mA, limited 32mA)
            #     time.sleep(0.01)

    # ---Stimulation---
    # Stimulates EMS on the inputted channel for the inputted number of pulses
    def stim(self, channel : int, intensity: int = None, pulse_width: int = None, pulse_count : int = 5) -> None:
        if intensity is None:
            intensity = self.calibration[channel][2]

        if pulse_width is None:
            pulse_width = self.calibration[channel][1]
        self.dev.stim(channel, intensity,pulse_width, pulse_count)

        
    def stim_time(self, channel : int, intensity: int, pulse_width: int, frequency : int, timer : int, pulse_count = None) -> None:
        if not intensity:
            intensity = self.calibration[channel][2]

        if not pulse_width:
            pulse_width = self.calibration[channel][1]


        # convert frequency into delay
        if frequency:
            self.delay = 1 / frequency

        # getting pulse_count for set stim duration
        if timer:            
            pulse_count = int(timer / self.delay)

        self.dev.stim(channel, intensity,pulse_width, pulse_count)


    # Stimulates EMS on the inputted channel with delay in msec
    def stim_after_delay(self, channel : int, intensity: int = None, pulse_width: int = None, pulse_count : int = 1, delay : int = 0, start_time : float = None) -> None:
        delay = delay / 1000 # convert msec to sec
        while time.time() - start_time < delay:
            continue
        self.stim(channel=channel, intensity=intensity, pulse_width=pulse_width, pulse_count=pulse_count)
        
    # ---Return params---
    # Get intensity for set channel
    def getIntensity(self, channel: int) -> None:
        return self.calibration[channel][2]
    
    # Get pulse width for set channel
    def getPulseWidth(self, channel: int) -> None:
        return self.calibration[channel][1]
    
    # ---Calibration---
    # Calibrates to a specific value
    def setCalib(self, channel : int, intensity : int, pulse_width : int) -> None:        
        self.calibration[channel][1] = max(pulse_width, 0)
        self.calibration[channel][2] = max(intensity, 0)
    
    # Increases a channel's intensity by 1
    def incrCalib(self, channel : int) -> None:
        self.calibration[channel][2] += 1
    
    # Decreases a channel's intensity by 1
    def decrCalib(self, channel : int) -> None:
        self.calibration[channel][2] -= 1
        self.calibration[channel][2] = max(self.calibration[channel][2], 0)

    # ---Saving Calibration to File---
    def saveCalibration(self) -> None:
        with open(self.calibFile, 'w') as file:
            for channel in self.calibration:
                file.write(','.join(map(str, channel)) + '\n')

