import pytest

from ems.devices import Device


class TestDevice(Device):
    name = "Test Device"

    intensity_min = 0
    intensity_max = 100
    intensity_step = 1

    pulse_width_min = 100
    pulse_width_max = 200
    pulse_width_step = 2

    n_channels = 4

    @classmethod
    def from_serial_device(cls, device):
        """Connect to a hypothetical serial device"""
        return cls(None)

    def stimulate(self, channel, intensity, pulse_width, validate_params=True):
        if validate_params:
            self.validate(channel, intensity, pulse_width)
        return True


def test_stimulate():
    dev = TestDevice(None)

    assert dev.stimulate(0, 50, 150, validate_params=True)

    with pytest.raises(ValueError):
        assert dev.stimulate(0, 201, 150, validate_params=True)
