#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk, LEFT, BOTH
from pydantic import confloat, conint
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
import scipy.signal.windows
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch04Group
from dcs.utils import swap_freq, abs_log_fft

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


@ui_create
class ConfigCh04QuantizationNoise(ConfigObject):
    _KEY = 'ch04_quantization_noise'

    freq: confloat(ge=0.0, lt=128.0, multiple_of=1.0) = 10.0
    amplitude: confloat(ge=0.0, lt=10.0, multiple_of=0.01) = 5.0

    adc_bits: conint(ge=1, lt=25) = 8
    adc_min: confloat(ge=-50.0, lt=0.0, multiple_of=0.1) = -5.0
    adc_max: confloat(ge=0.0, lt=50.0, multiple_of=0.1) = 5.0

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        frm1 = ttk.Frame(frm, borderwidth=1, relief='raised')
        frm1.pack()

        ttk.Label(frm1, text='Signal Frequency:').grid(row=0, column=0)
        w = self.ui_create_freq(frm1)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        ttk.Label(frm1, text='Signal Amplitude:').grid(row=1, column=0)
        w = self.ui_create_amplitude(frm1)
        frm.add_widget(w)
        w.grid(row=1, column=1)

        frm2 = ttk.Frame(frm, borderwidth=1, relief='raised')
        frm2.pack()

        ttk.Label(frm2, text='ADC Bits:').grid(row=0, column=0)
        w = self.ui_create_adc_bits(frm2)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        ttk.Label(frm2, text='ADC Min. Cut-off:').grid(row=1, column=0)
        w = self.ui_create_adc_min(frm2)
        frm.add_widget(w)
        w.grid(row=1, column=1)

        ttk.Label(frm2, text='ADC Max. Cut-off:').grid(row=2, column=0)
        w = self.ui_create_adc_max(frm2)
        frm.add_widget(w)
        w.grid(row=2, column=1)

        return frm

    def calc_signal(self, t: np.ndarray) -> np.ndarray:
        center_volt = (self.adc_max + self.adc_min) / 2
        step = (self.adc_max - self.adc_min) / np.power(2, self.adc_bits)
        volt = np.real(center_volt + (self.amplitude * np.exp(1j * 2 * np.pi * self.freq * t)))
        discrete = np.round(volt / step) + np.power(2, self.adc_bits - 1)
        discrete = np.where(discrete < 0, 0, discrete)
        upper_limit = np.power(2, self.adc_bits) - 1
        discrete = np.where(discrete > upper_limit, upper_limit, discrete)
        return discrete


class Ch04QuantizationNoiseFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh04QuantizationNoise = default_store().get_config(ConfigCh04QuantizationNoise)

        ctrl_frm = self._create_control()
        ctrl_frm.pack(side=LEFT)

        signal_frm = self._create_signal_canvas()
        signal_frm.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigControlFrame:
        frm: ConfigControlFrame = self._config.make_config_widget(self)
        frm.widgets_on_change(self._on_change)
        return frm

    def _on_change(self, _, __, ___):
        default_store().save()
        self.draw_signal()

    def _create_signal_canvas(self) -> ttk.Widget:
        frm = ttk.Frame(self)

        self._signal_fig = Figure(figsize=(12, 6), dpi=100)

        self._signal_canvas = FigureCanvasTkAgg(self._signal_fig, frm)
        self._signal_canvas.get_tk_widget().pack(expand=True, fill=BOTH)

        self.draw_signal()

        return frm

    def draw_signal(self):
        LENGTH = 2048

        self._signal_fig.clear()
        ax_td = self._signal_fig.add_subplot(2, 1, 1)
        ax_td.set_xlim(0.0, 1.0)
        ax_td.set_xlabel('time')
        ax_td.set_ylabel('value')
        ax_td.set_title('Time Domain')
        ax_fd = self._signal_fig.add_subplot(2, 1, 2)
        ax_fd.set_xlim(0, int(LENGTH/4))
        ax_fd.set_ylim(-180, 0)
        ax_fd.set_xlabel('frequency')
        ax_fd.set_ylabel('value (logarithmic)')
        ax_fd.set_title('Frequency Domain')

        t = np.arange(0, LENGTH, 1) / LENGTH
        f = swap_freq(np.fft.fftfreq(t.shape[-1], 1.0/LENGTH))

        sig_td = self._config.calc_signal(t)
        sig_td_norm = 2 * np.sqrt(2) * ((sig_td / np.power(2, self._config.adc_bits)) - 0.5)
        sig_fd = abs_log_fft(sig_td_norm * scipy.signal.windows.blackman(len(t)))

        ax_td.plot(t, sig_td, label='Quantized Signal', linestyle='solid', color='blue', linewidth=1)
        ax_td.legend()

        ax_fd.plot(f, sig_fd, label='Quantized Signal', linestyle='solid', color='blue', linewidth=1)
        ax_fd.legend()

        self._signal_fig.tight_layout()
        self._signal_canvas.draw()


class Ch04QuantizationNoiseWindow(Window):
    GROUP = Ch04Group
    TITLE = 'Quantization Noise'
    FRAME = Ch04QuantizationNoiseFrame


if __name__ == '__main__':
    Ch04QuantizationNoiseWindow.main()

