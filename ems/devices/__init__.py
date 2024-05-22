from .rehastim import Rehastim
from .rehamove import Rehamove
from .base import (
    Device,
    IntensityConfiguration,
    ChannelConfiguration,
    PulseWidthConfiguration,
)
from .dummy import Dummy

supported_devices = {"rehastim": Rehastim, "rehamove": Rehamove, "dummy": Dummy}
