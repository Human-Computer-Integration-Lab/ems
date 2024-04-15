class Device:
    name: str = None
    pulse_count: int = None
    min_intensity: int = None
    max_intensity: int = None
    min_pulse_width: int = None
    max_pulse_width: int = None
    min_channel: int = None
    max_channel: int = None

    #
    def __init__(self, serial_device):
        self.serial_device = serial_device

    @classmethod
    def from_port(cls, port, **kwargs):
        pass

    @classmethod
    def from_serial_device(cls, device):
        return cls(device)

    def stimulate(self, *args, **kwargs):
        # TODO: each device MUST have a stimulate method
        pass

    def validate(self, channel, intensity, pulse_width):
        """Validates a possible configuration against the device specifications."""
        self._validate_channel(channel)
        self._validate_intensity(intensity)
        self._validate_pulse_width(pulse_width)

    def _validate_intensity(self, intensity):
        """Checks if a provided intensity value is within the device specifications."""
        if intensity < self.min_intensity or intensity > self.max_intensity:
            raise ValueError(
                f"Invalid value for intensity: {intensity}. Value must be between {self.min_intensity} and {self.max_intensity}"
            )

    def _validate_pulse_width(self, pulse_width):
        """Checks if a provided pulse_width value is within the device specifications."""
        if pulse_width < self.min_pulse_width or pulse_width > self.max_pulse_width:
            raise ValueError(
                f"Invalid value for pulse_width: {pulse_width}. Value must be between {self.min_pulse_width} and {self.max_pulse_width}"
            )

    def _validate_channel(self, channel):
        """Checks if a provided channel value is within the device specifications."""
        if channel < self.min_channel or channel > self.max_channel:
            raise ValueError(
                f"Invalid value for channel: {channel}. Value must be between {self.min_channel} and {self.max_channel}"
            )
