class Device:
    name: str = None

    def __init__(self, device):
        """TODO:"""
        self.device = device

    @classmethod
    def from_port(cls, port, **kwargs):
        raise NotImplementedError

    @classmethod
    def from_serial_device(cls, device):
        return cls(device)

    def stimulate(self, *args, **kwargs):
        raise NotImplementedError

    def validate(self, **kwargs):
        if isinstance(self, IntensityConfiguration):
            self.validate_intensity(kwargs.get("intensity"))
        if isinstance(self, PulseWidthConfiguration):
            self.validate_pulse_width(kwargs.get("pulse_width"))
        if isinstance(self, ChannelConfiguration):
            self.validate_channel(kwargs.get("channel"))


class IntensityConfiguration:
    intensity_min: int = None
    intensity_max: int = None
    intensity_step: int = None

    def validate_intensity(self, intensity, **kwargs):
        """Checks if a provided intensity value is within the device specifications."""

        if intensity not in range(
            self.intensity_min,
            self.intensity_max + self.intensity_step,
            self.intensity_step,
        ):
            raise ValueError(
                f"Invalid value for intensity: {intensity}. Value must be between {self.intensity_min} and {self.intensity_max} with a step size of "
                f"{self.intensity_step}"
            )


class PulseWidthConfiguration:
    pulse_width_min: int = None
    pulse_width_max: int = None
    pulse_width_step: int = None

    def validate_pulse_width(self, pulse_width, **kwargs):
        """Checks if a provided pulse_width value is within the device specifications."""
        if pulse_width not in range(
            self.pulse_width_min,
            self.pulse_width_max + self.pulse_width_step,
            self.pulse_width_step,
        ):
            raise ValueError(
                f"Invalid value for pulse_width: {pulse_width}. Value must be between {self.pulse_width_min} and {self.pulse_width_max} with a step size of "
                f"{self.pulse_width_step}"
            )


class ChannelConfiguration:
    n_channels: int = None

    def validate_channel(self, channel, **kwargs):
        """Checks if a provided channel value is within the device specifications."""

        if channel < 0 or channel >= self.n_channels:
            raise ValueError(
                f"Invalid value for channel: {channel}. Device supports up to {self.n_channels} channels"
            )
