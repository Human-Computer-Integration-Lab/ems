# from core import EMS
from devices import Dummy
# my_device = EMS(Dummy(None))
# my_device.listen(5005)

x = Dummy.from_socket("localhost", 5000)

x.stimulate(0, 6, 300, 5)

print(x.exceptionalFunction())