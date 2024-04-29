import ipywidgets as widgets


class CalibrationWidget:
    def __init__(self, ems):
        self._ems = ems

        self.stim_button = widgets.Button(
            description="Stimulate", disabled=False, tooltip="Stimulate", icon="bolt"
        )

        self.set_button = widgets.Button(
            description="Set Pulse",
            disabled=False,
            tooltip="Set Pulse",
            icon="bookmark",
        )

        self.clear_button = widgets.Button(
            description="Clear",
            disabled=False,
            tooltip="Clear Channel",
            icon="eraser",
        )

        self.done_button = widgets.Button(
            description="Done", disabled=False, tooltip="Set Pulse", icon="check"
        )

        action_buttons = widgets.HBox(
            [self.stim_button, self.set_button, self.clear_button, self.done_button]
        )

        self.channel_buttons = widgets.ToggleButtons(
            options=[str(chan) for chan in range(0, self._ems.device.n_channels)],
            disabled=False,
            style={"button_width": "50px"},
        )

        self.intensity_slider = widgets.IntSlider(
            value=self._ems.device.intensity_min,
            min=self._ems.device.intensity_min,
            max=self._ems.device.intensity_max,
            step=self._ems.device.intensity_step,
            disabled=False,
            continuous_update=False,
            orientation="horizontal",
            readout=True,
            readout_format="d",
        )

        self.pulse_width_slider = widgets.IntSlider(
            value=self._ems.device.pulse_width_min,
            min=self._ems.device.pulse_width_min,
            max=self._ems.device.pulse_width_max,
            step=self._ems.device.pulse_width_step,
            disabled=False,
            continuous_update=False,
            orientation="horizontal",
            readout=True,
            readout_format="d",
        )

        self.widget = widgets.VBox(
            [
                widgets.HTML(value="Channels"),
                self.channel_buttons,
                widgets.HTML(value="Intensity (mA)"),
                self.intensity_slider,
                widgets.HTML(value="Pulse Width (μs)"),
                self.pulse_width_slider,
                widgets.HTML(value="Calibration Options"),
                action_buttons,
            ]
        )

        self.stim_button.on_click(self.on_stimulate_clicked)
        self.set_button.on_click(self.on_set_pulse_clicked)
        self.done_button.on_click(self.on_done_clicked)
        self.clear_button.on_click(self.on_clear_clicked)
        self.channel_buttons.observe(self.on_channel_clicked, "value")

    def on_stimulate_clicked(self, b):
        channel = int(self.channel_buttons.value)
        intensity = self.intensity_slider.value
        pulse_width = self.pulse_width_slider.value

        self._ems.stimulate(channel, intensity, pulse_width)

    def on_set_pulse_clicked(self, b):
        channel = int(self.channel_buttons.value)
        intensity = self.intensity_slider.value
        pulse_width = self.pulse_width_slider.value

        self._ems.set_pulse(channel, intensity, pulse_width)

    def on_clear_clicked(self, b):
        channel = int(self.channel_buttons.value)
        del self._ems.calibration[channel]

    def on_done_clicked(self, b):
        self.widget.close()

    def on_channel_clicked(self, change):
        channel = int(self.channel_buttons.value)

        if channel in self._ems.calibration:
            self.intensity_slider.value = self._ems.calibration[channel].intensity
            self.pulse_width_slider.value = self._ems.calibration[channel].pulse_width
        else:
            self.intensity_slider.value = self._ems.device.intensity_min
            self.pulse_width_slider.value = self._ems.device.pulse_width_min
