from .devices import Device, supported_devices


class EMS:
    def __init__(self, stimulator_handle: Device):
        """"""
        self.device = stimulator_handle

        self.calibration: dict[int, Channel] = {}

    def __repr__(self):
        pass

    @classmethod
    def autodetect(cls):
        # should be able to:
        # 1: detect what type of device is being connected and whether it is supported
        # 2. establish a connection
        pass

    @classmethod
    def from_port(cls, port, device_spec: str):
        if device_spec not in supported_devices:
            raise ValueError(
                f"TODO: {device_spec} is not a supported device. Expected one of {supported_devices.keys()}"
            )

        device_obj = supported_devices[device_spec]

        if not hasattr(device_obj, "from_port"):
            raise ValueError(
                f"TODO: {device_spec} does not support initialization from a serial port ... "
            )

        return cls(device_obj.from_port(port))

    @classmethod
    def from_serial_device(cls, device, device_spec: str):
        if device_spec not in supported_devices:
            raise ValueError(
                f"TODO: {device_spec} is not a supported device. Expected one of {supported_devices.keys()}"
            )

        device_obj = supported_devices[device_spec]

        if not hasattr(device_obj, "from_serial_device"):
            raise ValueError(
                f"TODO: {device_spec} does not support initialization from a serial device ... "
            )

        return cls(device_obj.from_serial_device(device))

    def calibrate(
        self,
        channel: int,
        intensity: int | list[int] = None,
        pulse_width: int | list[int] = None,
        pulse_count: int = 1,
        stimulate: bool = True,
    ):
        """Calibrates a specified channel for stimulation."""

        raise NotImplementedError

    def set_pulse(
        self, channel: int, intensity: int, pulse_width: int, pulse_count: int = 1
    ):
        if channel not in self.calibration:
            # initialize and store a channel
            self.calibration[channel] = Channel(
                identifier=channel,
                intensity=intensity,
                pulse_width=pulse_width,
                pulse_count=pulse_count,
                device=self.device,
            )
        else:
            # update existing values for a channel
            self.calibration[channel].intensity = intensity
            self.calibration[channel].pulse_width = pulse_width
            self.calibration[channel].pulse_count = pulse_count

    def load_calibration_file(self, file_path):
        # TODO
        # 1. read calibration file (i.e. json)
        # 2. repeated calls to calibrate with stimulate=False
        pass

    def save_calibration_file(self, file_path):
        # TODO
        # 1. for each channel in self.calibration, convert to JSON
        # 2. store as a single JSON
        pass

    def stimulate(
        self,
        channel: int,
        intensity: int = None,
        pulse_width: int = None,
        pulse_count: int = 1,
    ):
        """Stimulates a given channel ...

        Parameters
        ----------
        channel : int
            Channel identifier used to a select a channel to stimulate
        intensity: int, optional
            The intensity of the current used for stimulation, in milliAmperes (mA)
        pulse_width: int, optional
            The length of the pulse, in microseconds (μs)
        pulse_count: int, optional
            TODO
        """

        if intensity is None or pulse_width is None:
            # attempt to use a calibrated channel if intensity or pulse_width is not provided
            if channel not in self.calibration:
                raise ValueError(
                    f"Attempting to stimulate channel '{channel}', which is not calibrate. "
                    f"Please call .calibrate(channel={channel}, ...) before stimulating"
                )

        self.device.stimulate(channel, intensity, pulse_width, pulse_count)

    def timed_stimulate(self):
        pass

    def delayed_stimulate(self):
        pass


class Channel:
    """Docstring TODO"""

    def __init__(
        self,
        identifier: int,
        intensity: int | list[int],
        pulse_width: int | list[int],
        pulse_count: int,
        device: Device,
    ):
        """TODO:

        Support a custom waveform with a list of intensities and pulse widths ??
        """
        self._device = device

        # validate channel specifications to ensure they adhere to the device specifications
        self._device.validate(identifier, intensity, pulse_width)

        self._identifier = identifier
        self._intensity = intensity
        self._pulse_width = pulse_width
        self._pulse_count = pulse_count
        self._device = device

    def __repr__(self):
        pass

    @property
    def intensity(self):
        """The intensity of the current, in milliAmperes (mA)"""
        return self._intensity

    @intensity.setter
    def intensity(self, intensity):
        """Sets the intensity, with validations to ensure the provided intensity is within the device specifications."""
        self._device._validate_intensity(intensity)
        self._intensity = intensity

    @property
    def pulse_width(self):
        """The length of the pulse, in microseconds (μs)"""
        return self._pulse_width

    @pulse_width.setter
    def pulse_width(self, pulse_width):
        """Sets the pulse_width, with validations to ensure the provided pulse_width is within the device specifications."""
        self._device._validate_pulse_width(pulse_width)
        self._pulse_width = pulse_width

    @property
    def pulse_count(self):
        """The number of stimulation pulses to generate ?"""
        return self._pulse_count

    @pulse_count.setter
    def pulse_count(self, pulse_count):
        self._pulse_count = pulse_count

    def to_json(self):
        # convert channel info to json ?
        pass
