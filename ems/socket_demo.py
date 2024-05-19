# from core import EMS
from devices import Dummy
# my_device = EMS(Dummy(None))
# my_device.listen(5005)

x = Dummy(None)
x.setSecret(15)
x.listen_socket("localhost", 5000)

