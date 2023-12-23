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
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch03Group
from typing import List
from enum import Enum
import scipy.signal

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FunctionType(str, Enum):
    Cos = 'Cosine'
    Rect = 'Rectangular'
    Tri = 'Triangular'
    Gauss = 'Gaussian'


@ui_create
class FunctionSet(ConfigObject):
    function: FunctionType = FunctionType.Gauss
    amplitude: confloat(ge=0.0, lt=10.0, multiple_of=0.01) = 5.0
    width: confloat(ge=0.01, lt=1.0, multiple_of=0.01) = 0.5
    offset: confloat(ge=-5.0, lt=5.0, multiple_of=0.01) = 0.0

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Function:').grid(row=0, column=0)
        w = self.ui_create_function_dropdown(frm)
        w.grid(row=0, column=1)
        frm.add_widget(w)

        ttk.Label(frm, text='Amplitude:').grid(row=1, column=0)
        w = self.ui_create_amplitude(frm)
        w.grid(row=1, column=1)
        frm.add_widget(w)

        ttk.Label(frm, text='Width:').grid(row=2, column=0)
        w = self.ui_create_width(frm)
        w.grid(row=2, column=1)
        frm.add_widget(w)

        ttk.Label(frm, text='Offset:').grid(row=3, column=0)
        w = self.ui_create_offset(frm)
        w.grid(row=3, column=1)
        frm.add_widget(w)

        return frm


@ui_create
class ConfigCh03CrossCorrelation(ConfigObject):
    _KEY = 'ch03_cross'

    fn1: FunctionSet = FunctionSet()
    fn2: FunctionSet = FunctionSet()

    tau: confloat(ge=-1.0, lt=1.0, multiple_of=0.01) = 0.2
    sigma: confloat(ge=0, le=3.0, multiple_of=0.01) = 0.0

    random_seed: conint(ge=0, lt=10000) = 1000

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Function 1').pack()
        frm_fn1 = self.fn1.make_config_widget(frm)
        frm_fn1.pack()
        for w in frm_fn1.ctrl_widgets:
            frm.add_widget(w)

        ttk.Label(frm, text='Function 2').pack()
        frm_fn2 = self.fn2.make_config_widget(frm)
        frm_fn2.pack()
        for w in frm_fn2.ctrl_widgets:
            frm.add_widget(w)

        ttk.Label(frm_fn2, text='Tau (Shift):').grid(row=4, column=0)
        w = self.ui_create_tau(frm_fn2)
        w.grid(row=4, column=1)
        frm.add_widget(w)

        ttk.Label(frm_fn2, text='Standard Deviation:').grid(row=5, column=0)
        w = self.ui_create_sigma(frm_fn2)
        w.grid(row=5, column=1)
        frm.add_widget(w)

        frm_general = ttk.Frame(frm, borderwidth=1, relief='raised')
        frm_general.pack()

        ttk.Label(frm_general, text='Random Seed:').grid(row=1, column=0)
        w = self.ui_create_random_seed(frm_general)
        w.grid(row=1, column=1)
        frm.add_widget(w)

        return frm

    def _calc_cos(self, fn: FunctionSet, t: np.ndarray, shift: float) -> np.ndarray:
        phi = fn.amplitude * np.exp(1j * shift * 2 * np.pi) * np.exp(1j * 2 * np.pi * t / fn.width)
        return np.real(phi)

    def _calc_rect(self, fn: FunctionSet, t: np.ndarray, shift: float) -> np.ndarray:
        return np.where(np.abs(t - shift) < (fn.width / 2), fn.amplitude, 0)

    def _calc_tri(self, fn: FunctionSet, t: np.ndarray, shift: float) -> np.ndarray:
        saw = fn.amplitude * scipy.signal.sawtooth(2 * np.pi * ((t - shift) / fn.width))
        return np.where(np.abs(t - shift) < (fn.width / 2), np.abs(saw), 0)

    def _calc_gauss(self, fn: FunctionSet, t: np.ndarray, shift: float) -> np.ndarray:
        return fn.amplitude * np.exp(-1 * np.power((t - shift), 2) / (2 * np.power(fn.width, 2)))

    def calc_signal(self, fn: FunctionSet, t: np.ndarray, shift: float) -> np.ndarray:
        if fn.function == FunctionType.Cos:
            return fn.offset + self._calc_cos(fn, t, shift)
        elif fn.function == FunctionType.Rect:
            return fn.offset + self._calc_rect(fn, t, shift)
        elif fn.function == FunctionType.Tri:
            return fn.offset + self._calc_tri(fn, t, shift)
        elif fn.function == FunctionType.Gauss:
            return fn.offset + self._calc_gauss(fn, t, shift)
        else:
            raise KeyError

    def calc_noise(self, t: np.ndarray) -> np.ndarray:
        return np.random.normal(0, self.sigma, len(t))

    def calc_signal_1(self, t: np.ndarray) -> np.ndarray:
        return self.calc_signal(self.fn1, t, 0)

    def calc_signal_2(self, t: np.ndarray) -> np.ndarray:
        return self.calc_signal(self.fn2, t, self.tau) + self.calc_noise(t)


class Ch03CrossCorrelationFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh03CrossCorrelation = default_store().get_config(ConfigCh03CrossCorrelation)

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
        LENGTH = 200

        title = 'Auto Correlation' if self._config.sigma == 0 else 'Cross Correlation'

        np.random.seed(self._config.random_seed)

        self._signal_fig.clear()

        ax_inp = self._signal_fig.add_subplot(2, 1, 1)
        ax_cross = self._signal_fig.add_subplot(2, 1, 2)

        ax_inp.set_xlim(-1.2, 1.2)
        ax_inp.set_xlabel('time')
        ax_inp.set_ylabel('value')
        ax_inp.set_title('Signals')

        ax_cross.set_xlim(-1.2, 1.2)
        ax_cross.set_xlabel('time')
        ax_cross.set_ylabel('value')
        ax_cross.set_title(title)

        t = np.linspace(-1.0, 1.0, LENGTH)

        sig1 = self._config.calc_signal_1(t)
        sig2 = self._config.calc_signal_2(t)
        ax_inp.plot(t, sig1, label='Transmitted Signal', linestyle='solid', linewidth=1)
        ax_inp.plot(t, sig2, label='Received Signal', linestyle='solid', linewidth=1)
        ax_inp.legend()

        sig_cross = np.correlate(sig1, sig2, mode='same')
        ax_cross.plot(t, sig_cross, label=title, linestyle='solid', linewidth=1)
        ax_cross.legend()

        self._signal_canvas.draw()


class Ch03CrossCorrelationWindow(Window):
    GROUP = Ch03Group
    TITLE = 'Cross Correlation'
    FRAME = Ch03CrossCorrelationFrame


if __name__ == '__main__':
    Ch03CrossCorrelationWindow.main()

