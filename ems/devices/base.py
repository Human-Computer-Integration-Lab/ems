class Device:
    name: str = None

    # intensity configuration
    intensity_min: int = None
    intensity_max: int = None
    intensity_step: int = None

    # pulse width configuration
    pulse_width_min: int = None
    pulse_width_max: int = None
    pulse_width_step: int = None

    n_channels: int = None

    def __init__(self, serial_device):
        self.serial_device = serial_device

    @classmethod
    def from_port(cls, port, **kwargs):
        pass

    @classmethod
    def from_serial_device(cls, device):
        return cls(device)

    def stimulate(self, *args, **kwargs):
        raise NotImplementedError

    def validate(self, channel, intensity, pulse_width):
        """Validates a possible configuration against the device specifications."""
        self._validate_channel(channel)
        self._validate_intensity(intensity)
        self._validate_pulse_width(pulse_width)

    def _validate_intensity(self, intensity):
        """Checks if a provided intensity value is within the device specifications."""

        if intensity not in range(
            self.intensity_min,
            self.intensity_max + self.intensity_step,
            self.intensity_step,
        ):
            raise ValueError(
                f"Invalid value for intensity: {intensity}. Value must be between {self.intensity_min} and {self.intensity_max} with a step size of "
                f"{self.pulse_width_step}"
            )

    def _validate_pulse_width(self, pulse_width):
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

    def _validate_channel(self, channel):
        """Checks if a provided channel value is within the device specifications."""

        if channel < 0 or channel >= self.n_channels:
            raise ValueError(
                f"Invalid value for channel: {channel}. Device supports up to {self.n_channels} channels"
            )
