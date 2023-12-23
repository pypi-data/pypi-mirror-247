#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk, LEFT, BOTH
from pydantic import confloat
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch05Group
from dcs.utils import swap_freq, abs_log_fft
from typing import List
from enum import Enum

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


SAMPLE_LEN = 512
FFT_OVERSAMPLING = 64


@ui_create
class Function(ConfigObject):
    freq: confloat(ge=0.0, lt=SAMPLE_LEN/4, multiple_of=(4.0/FFT_OVERSAMPLING)) = 1.0
    amplitude: confloat(ge=0.0, lt=10.0, multiple_of=0.01) = 5.0
    phase: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0
    offset: confloat(ge=-5.0, lt=5.0, multiple_of=0.01) = 0.0

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent)

        ttk.Label(frm, text='Frequency:').grid(row=0, column=0)
        w = self.ui_create_freq(frm)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        ttk.Label(frm, text='Amplitude:').grid(row=1, column=0)
        w = self.ui_create_amplitude(frm)
        frm.add_widget(w)
        w.grid(row=1, column=1)

        ttk.Label(frm, text='Phase:').grid(row=2, column=0)
        w = self.ui_create_phase(frm)
        frm.add_widget(w)
        w.grid(row=2, column=1)
        ttk.Label(frm, text='°').grid(row=2, column=2)

        ttk.Label(frm, text='Offset:').grid(row=3, column=0)
        w = self.ui_create_offset(frm)
        frm.add_widget(w)
        w.grid(row=3, column=1)

        return frm

    def calc_signal(self, t: np.ndarray, phi_mod_deg: int | np.ndarray = 0) -> np.ndarray:
        phasor = self.amplitude * np.exp(1j * ((self.phase * np.pi / 180) + phi_mod_deg))
        phi = np.exp(1j * 2 * np.pi * self.freq * t)
        return np.real(self.offset + (phasor * phi))

    def make_title(self):
        return f'n={self.freq}, {self.amplitude}, {self.phase}°'


class ModulationMethod(str, Enum):
    AM_DSB_TC = 'Amplitude Modulation (DSB-TC)'
    AM_DSB_SC = 'Amplitude Modulation (DSB-SC)'
    PM = 'Phase Modulation'


@ui_create
class ConfigCh05Modulation(ConfigObject):
    _KEY = 'ch05_modulation'

    baseband_funcs: List[Function] = [
        Function(freq=1.0, amplitude=1.0),
        Function(freq=1.5, amplitude=1.0),
    ]
    carrier: Function = Function(freq=10.0, amplitude=5.0)
    method: ModulationMethod = ModulationMethod.AM_DSB_TC
    am_mod_index: confloat(ge=0.0, lt=10.0, multiple_of=0.01) = 0.5
    pm_mod_index: confloat(ge=0.0, lt=10.0, multiple_of=0.00001) = 0.5

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Functions:').pack()
        w = self.ui_create_baseband_funcs_list(frm, lambda e: e.make_title())
        frm.add_widget(w)
        w.pack()

        frm2 = ttk.Frame(frm, borderwidth=1, relief='raised')
        frm2.pack()
        ttk.Label(frm2, text='Carrier:').pack()
        carrier_frm = self.carrier.make_config_widget(frm2)
        for w in carrier_frm.ctrl_widgets:
            frm.add_widget(w)
        carrier_frm.pack()

        frm1 = ttk.Frame(frm)
        frm1.pack()

        ttk.Label(frm1, text='Modulation Method:').grid(row=0, column=0)
        w = self.ui_create_method_dropdown(frm1)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        ttk.Label(frm1, text='AM Modulation Index:').grid(row=1, column=0)
        w = self.ui_create_am_mod_index(frm1)
        frm.add_widget(w)
        w.grid(row=1, column=1)

        ttk.Label(frm1, text='PM Modulation Index:').grid(row=2, column=0)
        w = self.ui_create_pm_mod_index(frm1)
        frm.add_widget(w)
        w.grid(row=2, column=1)

        return frm

    def calc_baseband_signal(self, t: np.ndarray) -> np.ndarray:
        x = np.zeros((len(self.baseband_funcs), len(t)))
        for index, func in enumerate(self.baseband_funcs):
            x[index, :] = func.calc_signal(t)
        return np.sum(x, axis=0)

    def calc_carrier_signal(self, t: np.ndarray, phi_mod_deg: int | np.ndarray = 0) -> np.ndarray:
        return self.carrier.calc_signal(t, phi_mod_deg)

    def _calc_am_dsb_tc(self, t: np.ndarray) -> np.ndarray:
        return self.calc_carrier_signal(t) * (1 + (self.am_mod_index * self.calc_baseband_signal(t)))

    def _calc_am_dsb_sc(self, t: np.ndarray) -> np.ndarray:
        return self.calc_carrier_signal(t) * self.am_mod_index * self.calc_baseband_signal(t)

    def _calc_pm(self, t: np.ndarray) -> np.ndarray:
        phi_mod_deg = 2 * np.pi * self.pm_mod_index * self.calc_baseband_signal(t)
        return self.calc_carrier_signal(t, phi_mod_deg)

    def calc_modulated(self, t: np.ndarray) -> np.ndarray:
        if self.method == ModulationMethod.AM_DSB_TC:
            return self._calc_am_dsb_tc(t)
        elif self.method == ModulationMethod.AM_DSB_SC:
            return self._calc_am_dsb_sc(t)
        elif self.method == ModulationMethod.PM:
            return self._calc_pm(t)
        else:
            raise Exception('Unknown modulation method')


class Ch05ModulationFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh05Modulation = default_store().get_config(ConfigCh05Modulation)

        ctrl_frm = self._create_control()
        ctrl_frm.pack(side=LEFT)

        signal_frm = self._create_signal_canvas()
        signal_frm.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigControlFrame:
        frm = self._config.make_config_widget(self)
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
        self._signal_fig.clear()

        ax_inp = self._signal_fig.add_subplot(3, 1, 1)
        ax_inp.set_xlim(0.0, 1.0)
        ax_inp.set_xlabel('time')
        ax_inp.set_ylabel('value')
        ax_inp.set_title('Input Signals')
        ax_mod = self._signal_fig.add_subplot(3, 1, 2)
        ax_mod.set_xlim(0.0, 1.0)
        ax_mod.set_xlabel('time')
        ax_mod.set_ylabel('value')
        ax_mod.set_title('Modulated Signal')
        ax_fft = self._signal_fig.add_subplot(3, 1, 3)
        ax_fft.set_xlim(0, int(SAMPLE_LEN/4))
        ax_fft.set_xlabel('frequency')
        ax_fft.set_ylabel('value (logarithmic)')
        ax_fft.set_title('Frequency-Domain')

        t = np.arange(0, SAMPLE_LEN, 1) / SAMPLE_LEN
        t_ovs = np.arange(0, (SAMPLE_LEN * FFT_OVERSAMPLING), 1) / SAMPLE_LEN

        f_ovs = swap_freq(np.fft.fftfreq(t_ovs.shape[-1], 1.0/SAMPLE_LEN))

        ax_inp.plot(t, self._config.calc_baseband_signal(t), label='Baseband', linestyle='solid', color='blue', linewidth=1)
        ax_inp.plot(t, self._config.calc_carrier_signal(t), label='Carrier', linestyle='solid', color='red', linewidth=1)
        ax_inp.legend()

        ax_mod.plot(t, self._config.calc_modulated(t), label='Modulated', linestyle='solid', color='green', linewidth=1)
        ax_mod.legend()

        ax_fft.plot(f_ovs, abs_log_fft(self._config.calc_baseband_signal(t_ovs)), label='Baseband', linestyle='solid', color='blue', linewidth=1)
        ax_fft.plot(f_ovs, abs_log_fft(self._config.calc_carrier_signal(t_ovs)), label='Carrier', linestyle='solid', color='red', linewidth=1)
        ax_fft.plot(f_ovs, abs_log_fft(self._config.calc_modulated(t_ovs)), label='Modulated', linestyle='solid', color='green', linewidth=1)
        ax_fft.legend()

        self._signal_fig.tight_layout()

        self._signal_canvas.draw()


class Ch05ModulationWindow(Window):
    GROUP = Ch05Group
    TITLE = 'Modulation'
    FRAME = Ch05ModulationFrame


if __name__ == '__main__':
    Ch05ModulationWindow.main()

