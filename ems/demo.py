from core import EMS
import time
my_device = EMS.guided_setup()
my_device.set_pulse(1, 6, 200)
my_device.save_calibration_file("user_calibration.json")


# my_device.device.device.version()
# my_device.stimulate(channel=1, intensity=6, pulse_width=10)
my_device.calibrate(1, pulse_width=300, pulse_count=10)
time.sleep(1)