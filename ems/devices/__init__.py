from .rehastim import Rehastim
from .rehamove import RehamoveSerial
from .base import Device
from .dummy import Dummy

supported_devices = {"rehastim": Rehastim, "rehamove": RehamoveSerial, "dummy": Dummy}

__all__ = [
    "Device",
    "Rehastim",
    "Rehamove",
    "Dummy",
    "supported_devices",
]
