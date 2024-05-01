from devices import Device, supported_devices
from calibration import CalibrationWidget
import json
import time
import json
from IPython.display import display


class EMS:
    """A device-agnostic interface for performing Electrical Muscle Stimulation.

    Parameters
    ----------
    stimulator_handle: Device
        Reference to the hardware device that will be used for stimulation

     See Also
    --------
    EMS.from_port
    EMS.from_serial_device

    """

    def __init__(self, stimulator_handle: Device):
        self.device = stimulator_handle

        self.calibration: dict[int, Channel] = {}

    def __repr__(self):
        #  TODO: add better alignment

        repr_str = "<ems.EMS>\n"
        repr_str += "Device Information:\n"
        repr_str += f" * Name:  {self.device.name}\n"

        repr_str += "Channel Information (intensity, pulse_width):\n"
        for channel in range(0, self.device.n_channels):
            if channel in self.calibration:
                repr_str += f" * Channel {channel}:     ({self.calibration[channel].intensity}mA, {self.calibration[channel].pulse_width}μs)\n"
            else:
                repr_str += f" * Channel {channel}:     Not Calibrated\n"

        return repr_str

    @classmethod
    def autodetect(cls):
        # should be able to:
        # 1: detect what type of device is being connected and whether it is supported
        # 2. establish a connection
        raise NotImplementedError

    @classmethod
    def from_device(cls, device: Device):
        """Construct an EMS instance from a user-specified Device."""

        if not isinstance(device, Device):
            raise ValueError("TODO")

        return cls(device)

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


    @classmethod
    def guided_setup(cls):
        requested_class = select_option(supported_devices)
        return cls(requested_class.guided_setup())

    def visual_calibrate(
        self,
    ):
        """Calibration utility."""
        calibration_widget = CalibrationWidget(self)
        display(calibration_widget.widget)

    def set_pulse(self, channel: int, intensity: int, pulse_width: int):
        if channel not in self.calibration:
            # initialize and store a channel
            self.calibration[channel] = Channel(
                identifier=channel,
                intensity=intensity,
                pulse_width=pulse_width,
                device=self.device,
            )
        else:
            # update existing values for a channel
            self.calibration[channel].intensity = intensity
            self.calibration[channel].pulse_width = pulse_width

    def load_calibration_file(self, file_path):
        # raise NotImplementedError
        with open(file_path, "r") as file:
            # Read the content of the file into a string
            file_content = file.read()

        json_data = json.loads(file_content)
        for key, data in json_data.items():
            self.set_pulse(
                int(key),
                int(data["intensity"]),
                int(data["pulse_width"]),
                int(data["pulse_count"]),
            )
        # TODO
        # 1. read calibration file (i.e. json)
        # 2. repeated calls to calibrate with stimulate=False

    def save_calibration_file(self, file_path):
        # raise NotImplementedError
        # TODO
        # 1. for each channel in self.calibration, convert to JSON
        # 2. store as a single JSON
        json_data = {key: channel.to_dict() for key, channel in self.calibration.items()}
        json_string = json.dumps(json_data, indent=4)
        with open(file_path, 'w') as file:
            # Write the content to the file
            file.write(json_string)


    def _check_channel_calibration(self, channel, intensity, pulse_width):
        """Docstring TODO"""
        if intensity is None or pulse_width is None:
            # attempt to use a calibrated channel if intensity or pulse_width is not provided
            if channel not in self.calibration:
                raise ValueError(
                    f"Attempting to stimulate channel '{channel}', which is not calibrated. "
                    f"Please call .calibrate(channel={channel}, ...) before stimulating or "
                    f"explicitly specify the 'intensity' and 'pulse_width'"
                )

    def stimulate(
        self,
        channel: int,
        intensity: int = None,
        pulse_width: int = None,
    ):
        """Stimulates a single pulse.

        Parameters
        ----------
        channel : int
            Channel identifier used to a select a channel to stimulate
        intensity: int, optional
            The intensity of the current used for stimulation, in milliAmperes (mA)
        pulse_width: int, optional
            The length of the pulse, in microseconds (μs)
        """
        self._check_channel_calibration(channel, intensity, pulse_width)

        if intensity is None:
            intensity = self.calibration[channel].intensity
        if pulse_width is None:
            pulse_width = self.calibration[channel].pulse_width

        self.device.stimulate(
            channel=channel, intensity=intensity, pulse_width=pulse_width, pulse_count=1
        )

    def pulsed_stimulate(
        self,
        channel: int,
        intensity: int = None,
        pulse_width: int = None,
        pulse_count: int = 3,
        delay: int = 0.005,
    ):
        """Stimulates multiple pulses seperated by a given delay.

        Parameters
        ----------
        channel : int
            Channel identifier used to a select a channel to stimulate
        intensity: int, optional
            The intensity of the current used for stimulation, in milliAmperes (mA)
        pulse_width: int, optional
            The length of the pulse, in microseconds (μs)
        pulse_count: int, optional
            The number of pulses to stimulate
        delay: int, optional
            The delay between each pulse (in seconds)
        """
        self._check_channel_calibration(channel, intensity, pulse_width)

        for _ in range(pulse_count):
            self.device.stimulate(channel, intensity, pulse_width)
            time.sleep(delay)

    def timed_stimulate(self):
        raise NotImplementedError

    def delayed_stimulate(
        self,
        channel: int,
        intensity: int = None,
        pulse_width: int = None,
        delay: int = 2,
    ):
        """Stimulates a single pulse after some delay

        Parameters
        ----------
        channel : int
            Channel identifier used to a select a channel to stimulate
        intensity: int, optional
            The intensity of the current used for stimulation, in milliAmperes (mA)
        pulse_width: int, optional
            The length of the pulse, in microseconds (μs)
        delay: int, optional
            The delay between each pulse (in seconds)
        """
        self._check_channel_calibration(channel, intensity, pulse_width)
        time.sleep(delay)
        self.device.stimulate(channel, intensity, pulse_width)


class Channel:
    """Docstring TODO"""

    def __init__(
        self,
        identifier: int,
        intensity: int,
        pulse_width: int,
        device: Device,
    ):
        self._device = device

        # validate channel specifications to ensure they adhere to the device specifications
        self._device.validate(identifier, intensity, pulse_width)

        self._identifier = identifier
        self._intensity = intensity
        self._pulse_width = pulse_width
        self._device = device

    def __repr__(self):
        raise NotImplementedError

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
        """Sets the pulse_width, with validations to ensure the provided pulse_width is within the device
        specifications."""
        self._device._validate_pulse_width(pulse_width)
        self._pulse_width = pulse_width

    def to_json(self):
        # convert channel info to json ?
        raise NotImplementedError

    def to_dict(self) -> dict:
        """Convert Channel object to dictionary."""
        return {
            "intensity": self._intensity,
            "pulse_width": self._pulse_width,
        }


# Helper functions for the guided setup options
def display_options(dictionary):
    print("Choose the device type which you'd like to initialize:")
    for i, key in enumerate(dictionary.keys(), 1):
        print(f"{i}. {key}")


def select_option(dictionary):
    while True:
        display_options(dictionary)
        choice = input("Enter the number of your choice: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(dictionary):
                return dictionary[list(dictionary.keys())[choice - 1]]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
