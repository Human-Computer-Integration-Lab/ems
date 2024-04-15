from .devices import Device


class EMS:
    def __init__(self, stimulator_handle: Device):
        """"""
        self.device = stimulator_handle

        # a dictionary of channel ids to channel instances (ADD TYPING)
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
        pulse_count: int = 1,
        stimulate: bool = True,
    ):
        """Calibrates a specified channel for stimulation."""

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

        if stimulate:
            # stimulate the pulse for calibration
            self.stimulate(channel, intensity, pulse_width, pulse_count)

    def load_calibration_file(self, file_path):
        # TODO
        pass

    def save_calibration_file(self, file_path):
        # TODO
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
        """The intensity of the current, in milliAmperes (mA)"""
        return self._intensity

    @intensity.setter
    def intensity(self, intensity):
        self._device._validate_intensity(intensity)
        self._intensity = intensity

    @property
    def pulse_width(self):
        """The length of the pulse, in microseconds (μs)"""
        return self._pulse_width

    @pulse_width.setter
    def pulse_width(self, pulse_width):
        self._device._validate_pulse_width(pulse_width)
        self._pulse_width = pulse_width

    @property
    def pulse_count(self):
        """The number of stimulation pulses to generate?"""
        return self._pulse_count

    @pulse_count.setter
    def pulse_count(self, pulse_count):
        self._device._validate_pulse_count(pulse_count)
        self._pulse_count = pulse_count

    def to_json(self):
        # convert channel info to json ?
        pass
