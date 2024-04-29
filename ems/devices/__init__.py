from .rehastim import Rehastim
from .base import Device

supported_devices = {"rehastim": Rehastim}

__all__ = [
    "Device",
    "Rehastim",
    "supported_devices",
]
