# from core import EMS
from devices import Dummy
# my_device = EMS(Dummy(None))
# my_device.listen(5005)

x = Dummy.from_osc("127.0.0.1", 5005)

x.stimulate(0, 300, 20, 5)

x.battery()

