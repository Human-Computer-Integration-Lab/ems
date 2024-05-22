from .rehastim import Rehastim
from .rehamove import Rehamove
from .dummy import Dummy

supported_devices = {"rehastim": Rehastim, "rehamove": Rehamove, "dummy": Dummy}
