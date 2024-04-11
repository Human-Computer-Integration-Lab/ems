from .devices import Device


class EMS:
    def __init__(self, stimulator_handle: Device):
        self.device = stimulator_handle

        self.calibration = {}

    def __repr__(self):
        pass

    @classmethod
    def autodetect(cls):
        pass

    @classmethod
    def from_port(cls):
        pass

    @classmethod
    def from_serial_device(cls):
        pass

    def calibrate(
        self,
        channel: int,
        intensity: int = None,
        pulse_width: int = None,
        pulse_count: int = 5,
    ):
        pass

    def stimulate(
        self,
        channel: int,
        intensity: int = None,
        pulse_width: int = None,
        pulse_count: int = 5,
    ):
        pass

    def timed_stimulate(self):
        pass

    def delayed_stimulate(self):
        pass


class Channel:
    def __init__(
        self,
        identifier: int,
        intensity: int,
        pulse_width: int,
        pulse_count: int,
        device: Device,
    ):
        self._identifier = identifier
        self._intensity = intensity
        self._pulse_width = pulse_width
        self._pulse_count = pulse_count
        self._device = device

    def __repr__(self):
        pass

    @property
    def intensity(self):
        return self._intensity

    @intensity.setter
    def intensity(self, intensity):
        # add checks to validate the range based on device specifications
        self._intensity = intensity

    @property
    def pulse_width(self):
        return self._pulse_width

    @pulse_width.setter
    def pulse_width(self, pulse_width):
        # add checks to validate the range based on device specifications
        self._pulse_width = pulse_width

    @property
    def pulse_count(self):
        return self._pulse_count

    @pulse_count.setter
    def pulse_count(self, pulse_count):
        self._pulse_count = pulse_count
