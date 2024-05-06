from core import EMS
from devices import Dummy
my_device = EMS.guided_setup()
my_device.device.version()
my_device.calibrate(0, 300, 10)


# my_device.listen(5005)

