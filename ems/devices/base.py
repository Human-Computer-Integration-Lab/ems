class Device:
    name: str = None
    intensity_conf: tuple | set = None
    pulse_width_conf: tuple | set = None
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

        if isinstance(self.intensity_conf, tuple):
            if intensity < self.intensity_conf[0] or intensity > self.intensity_conf[1]:
                raise ValueError(
                    f"Invalid value for intensity: {intensity}. Value must be between {self.intensity_conf[0]} and {self.intensity_conf[1]}"
                )
        else:
            if intensity not in self.intensity_conf:
                raise ValueError(
                    f"Invalid value for intensity: {intensity}. Value must be one of: {self.intensity_conf}"
                )

    def _validate_pulse_width(self, pulse_width):
        """Checks if a provided pulse_width value is within the device specifications."""
        if isinstance(self.pulse_width_conf, tuple):
            if (
                pulse_width < self.pulse_width_conf[0]
                or pulse_width > self.pulse_width_conf[1]
            ):
                raise ValueError(
                    f"Invalid value for pulse_width: {pulse_width}. Value must be between {self.pulse_width_conf[0]} and {self.pulse_width_conf[1]}"
                )
        else:
            if pulse_width not in self.pulse_width_conf:
                raise ValueError(
                    f"Invalid value for pulse_width: {pulse_width}. Value must be one of: {self.pulse_width_conf}"
                )

    def _validate_channel(self, channel):
        """Checks if a provided channel value is within the device specifications."""

        if channel < 0 or channel >= self.n_channels:
            raise ValueError(
                f"Invalid value for channel: {channel}. Device supports up to {self.n_channels} channels"
            )
