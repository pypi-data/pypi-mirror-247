#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk, Listbox, LEFT, BOTH
from pydantic import confloat, conint
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
from scipy.interpolate import make_interp_spline
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch04Group
from typing import List
from enum import Enum

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


@ui_create
class Function(ConfigObject):
    freq: confloat(ge=0.0, lt=128.0, multiple_of=0.01) = 1.0
    amplitude: confloat(ge=0.0, lt=10.0, multiple_of=0.01) = 5.0
    phase: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0
    offset: confloat(ge=-5.0, lt=5.0, multiple_of=0.01) = 0.0

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Frequency:').grid(row=0, column=0)
        self.ui_create_freq(frm).grid(row=0, column=1)

        ttk.Label(frm, text='Amplitude:').grid(row=1, column=0)
        self.ui_create_amplitude(frm).grid(row=1, column=1)

        ttk.Label(frm, text='Phase:').grid(row=2, column=0)
        self.ui_create_phase(frm).grid(row=2, column=1)
        ttk.Label(frm, text='°').grid(row=2, column=2)

        ttk.Label(frm, text='Offset:').grid(row=3, column=0)
        self.ui_create_offset(frm).grid(row=3, column=1)

        return frm

    def calc_signal(self, t: np.ndarray) -> np.ndarray:
        phasor = self.amplitude * np.exp(1j * self.phase * np.pi / 180)
        phi = np.exp(1j * 2 * np.pi * self.freq * t)
        return np.real(self.offset + (phasor * phi))

    def make_title(self):
        return f'n={self.freq}, {self.amplitude}, {self.phase}°'


class QuantizationMethod(str, Enum):
    Off = 'Off'
    Linear = 'Linear'


@ui_create
class Quantization(ConfigObject):
    method: QuantizationMethod = QuantizationMethod.Off
    adc_min: confloat(ge=-50.0, lt=0.0, multiple_of=0.1) = -5.0
    adc_max: confloat(ge=0.0, lt=50.0, multiple_of=0.1) = 5.0
    adc_bits: conint(ge=1, lt=9) = 2

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent)

        ttk.Label(frm, text='Method:').grid(row=0, column=0)
        w = self.ui_create_method_dropdown(frm)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        ttk.Label(frm, text='ADC Min. Cut-off:').grid(row=1, column=0)
        w = self.ui_create_adc_min(frm)
        frm.add_widget(w)
        w.grid(row=1, column=1)

        ttk.Label(frm, text='ADC Max. Cut-off:').grid(row=2, column=0)
        w = self.ui_create_adc_max(frm)
        frm.add_widget(w)
        w.grid(row=2, column=1)

        ttk.Label(frm, text='ADC Bits:').grid(row=3, column=0)
        w = self.ui_create_adc_bits(frm)
        frm.add_widget(w)
        w.grid(row=3, column=1)

        return frm

    def discrete_vals(self) -> np.ndarray:
        if self.method == QuantizationMethod.Linear:
            return np.linspace(self.adc_min, self.adc_max, 2**self.adc_bits)
        else:
            return np.array([0])

    def quantize(self, x: np.ndarray) -> np.ndarray:
        q = np.zeros((len(x), 2))
        if self.method == QuantizationMethod.Linear:
            v = self.discrete_vals()
            for idx in range(len(x)):
                q[idx, 0] = np.unravel_index(np.argmin(np.abs(x[idx] - v)), v.shape)[0]
                q[idx, 1] = v[int(q[idx, 0])]
        else:
            q[:, 0] = x
            q[:, 1] = x
        return q


class ConfigCh04SamplingFrame(ConfigControlFrame):
    wdg_sampling_freq: ttk.Spinbox
    wdg_sampling_phase: ttk.Spinbox
    wdg_funcs: Listbox
    frame_quantization: ConfigControlFrame


@ui_create
class ConfigCh04Sampling(ConfigObject):
    _KEY = 'ch04_sampling'

    sampling_freq: confloat(ge=1.0, lt=128.0, multiple_of=0.01) = 1.0
    sampling_phase: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0
    functions: List[Function] = [
        Function(freq=1.0, amplitude=5.0),
        Function(freq=1.5, amplitude=5.0),
        Function(freq=10.0, amplitude=5.0),
    ]
    quantization: Quantization = Quantization()

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigCh04SamplingFrame(parent, borderwidth=1, relief='raised')

        frm1 = ttk.Frame(frm)
        frm1.pack()

        ttk.Label(frm1, text='Sampling Frequency:').grid(row=0, column=0)
        frm.wdg_sampling_freq = self.ui_create_sampling_freq(frm1)
        frm.wdg_sampling_freq.grid(row=0, column=1)

        ttk.Label(frm1, text='Sampling Phase:').grid(row=1, column=0)
        frm.wdg_sampling_phase = self.ui_create_sampling_phase(frm1)
        frm.wdg_sampling_phase.grid(row=1, column=1)
        ttk.Label(frm1, text='°').grid(row=1, column=2)

        ttk.Label(frm, text='Functions:').pack()
        frm.wdg_funcs = self.ui_create_functions_list(frm, lambda e: e.make_title())
        frm.wdg_funcs.pack()

        frm2 = ConfigCh04SamplingFrame(frm, borderwidth=1, relief='raised')
        frm2.pack()
        ttk.Label(frm2, text='Quantization:').pack()
        frm.frame_quantization = self.quantization.make_config_widget(frm2)
        frm.frame_quantization.pack()

        return frm


class Ch04SamplingFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh04Sampling = default_store().get_config(ConfigCh04Sampling)

        self.quant_out = ttk.Label(self, text='')

        ctrl_frm = self._create_control()
        ctrl_frm.pack(side=LEFT)

        signal_frm = self._create_signal_canvas()
        signal_frm.pack(expand=True, fill=BOTH)

        self.quant_out.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigCh04SamplingFrame:
        frm: ConfigCh04SamplingFrame = self._config.make_config_widget(self)
        frm.wdg_sampling_freq.listen_change(self._on_change)
        frm.wdg_sampling_phase.listen_change(self._on_change)
        frm.wdg_funcs.listen_change(self._on_change)
        frm.frame_quantization.widgets_on_change(self._on_change)
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
        LENGTH = 512

        self._signal_fig.clear()
        ax_analog = self._signal_fig.add_subplot(2, 1, 1)
        ax_analog.set_xlim(-1.2, 1.2)
        ax_analog.set_xlabel('time')
        ax_analog.set_ylabel('value')
        ax_analog.set_title('Analogue Signal')
        ax_digital = self._signal_fig.add_subplot(2, 1, 2)
        ax_digital.set_xlim(-1.2, 1.2)
        ax_digital.set_xlabel('time')
        ax_digital.set_ylabel('value')
        if self._config.quantization.method == QuantizationMethod.Off:
            ax_digital.set_title('Sampled Signal')
        else:
            ax_digital.set_title('Digital Signal')

        t = np.linspace(-1.0, 1.01, LENGTH)
        t_sampled = np.arange(-1.0 + (self._config.sampling_phase/(self._config.sampling_freq * 360)), 1.01, 1/(self._config.sampling_freq))

        x = np.zeros((len(self._config.functions), len(t)))
        x_sampled = np.zeros((len(self._config.functions), len(t_sampled)))

        for index, func in enumerate(self._config.functions):
            x[index, :] = func.calc_signal(t)
            x_sampled[index, :] = func.calc_signal(t_sampled)
        func = np.sum(x, axis=0)
        func_sampled = np.sum(x_sampled, axis=0)

        quant_val = self._config.quantization.discrete_vals()
        quant_val = np.array([quant_val, quant_val])
        func_quant = self._config.quantization.quantize(func_sampled)

        if len(t_sampled) > 5:
            x_interp = make_interp_spline(t_sampled, func_quant[:, 1])
            t_interp = np.linspace(t_sampled.min(), t_sampled.max(), LENGTH)
            func_interp = x_interp(t_interp)
        else:
            t_interp = np.zeros((0,))
            func_interp = np.zeros((0,))

        ax_analog.plot(t, func, label='Function', linestyle='solid', linewidth=1)
        ax_analog.plot(t_sampled, func_sampled, label='Sampled', marker='x', linestyle='none', linewidth=1)
        ax_analog.legend()

        point_label = 'Sampled' if self._config.quantization.method == QuantizationMethod.Off else 'Quantized'

        ax_digital.plot(t_interp, func_interp, label='Interpolated', linestyle='dashed', linewidth=1)
        ax_digital.plot(t_sampled, func_quant[:, 1], label=point_label, marker='x', linestyle='none', linewidth=1)
        ax_digital.legend()

        if self._config.quantization.method != QuantizationMethod.Off:
            ax_analog.plot(np.array([-1, 1]), quant_val, label='Quantization Value', linestyle='dotted', linewidth=1)
            ax_digital.plot(np.array([-1, 1]), quant_val, label='Quantization Value', linestyle='dotted', linewidth=1)

            v_str = ', '.join([str(int(x)) for x in list(func_quant[:, 0])])
            self.quant_out.configure(text=f'Quantized = [{v_str}]')
        else:
            self.quant_out.configure(text='')

        self._signal_canvas.draw()


class Ch04SamplingWindow(Window):
    GROUP = Ch04Group
    TITLE = 'Sampling'
    FRAME = Ch04SamplingFrame


if __name__ == '__main__':
    Ch04SamplingWindow.main()

