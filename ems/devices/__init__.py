from .rehastim import Rehastim
from .rehamove import Rehamove
from .base import Device
from .dummy import Dummy

supported_devices = {"rehastim": Rehastim, "rehamove": Rehamove, "dummy": Dummy}

__all__ = [
    "Device",
    "Rehastim",
    "Rehamove",
    "Dummy",
    "supported_devices",
]
