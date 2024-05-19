from pythonosc import dispatcher, osc_server
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import SimpleUDPClient
import threading
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

    # OSC Client Configuration
    # Used to determine how this "device" will forward on commands 
    # to a remote device. 

    intercept: bool = False
    client = None

    def __init__(self, device):
        self.device = device

    def __getattribute__(self, name):
        print("Getattribute called with name: ", name)
        try:
            attr = super().__getattribute__(name)
            if not super().__getattribute__('intercept'):
                return attr
            if callable(attr):
                def method(*args):
                    # Use super() to access _send_osc_message to avoid recursion
                    super(Device, self).__getattribute__('_send_osc_message')(name, *args)
                return method
            return attr
        except AttributeError:
            # If the attribute does not exist, it will be handled in __getattr__
            raise    

    # def __getattr__(self, name):
    #     print("I'm called")
    #     if self.intercept:
    #         def method(*args):
    #             self._send_osc_message(name, *args)
    #         return method
    #     else:
    #         # Check if the method exists in the class
    #         print("Not intercepting")
    #         if hasattr(self, f"_actual_{name}"):
    #             return getattr(self, f"_actual_{name}")
    #         else:
    #             raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    @classmethod
    def from_port(cls, port, **kwargs):
        raise NotImplementedError

    @classmethod
    def from_serial_device(cls, device):
        return cls(device)
    
    @classmethod 
    def from_osc(cls, ip_address, port):
        x = cls(None)
        x.intercept = True
        x.client = SimpleUDPClient(ip_address, port)
        return x
    
    def _send_osc_message(self, method_name, *args):

        msg = OscMessageBuilder(address=f"/{method_name}")
        for arg in args:
            msg.add_arg(arg)
        msg = msg.build()
        self.client.send(msg)

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
                f"{self.intensity_step}"
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
        

    def listen(self, port):
        osc_dispatcher = dispatcher.Dispatcher()
        osc_dispatcher.set_default_handler(self.osc_handler)
        server_thread = threading.Thread(target=self.start_osc_server, args=(port, osc_dispatcher))
        server_thread.start()

    def osc_handler(self, address, *args):
            method_name = address.strip('/')
            if hasattr(self, method_name) and callable(getattr(self, method_name)):
                getattr(self, method_name)(*args)
            else:
                print("Couldn't find method: ", method_name)

    def start_osc_server(self, port, osc_dispatcher):
        server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", port), osc_dispatcher)
        print("OSC Server listening on port", port)
        server.serve_forever()
