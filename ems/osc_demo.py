from core import EMS
from devices import Dummy

my_device = EMS(Dummy(None))
my_device.listen(5005)
