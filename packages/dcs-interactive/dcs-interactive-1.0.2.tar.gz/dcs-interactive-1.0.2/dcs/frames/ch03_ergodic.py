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
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch03Group
from typing import List

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


@ui_create
class Function(ConfigObject):
    freq_mult: conint(ge=0, lt=3) = 0
    amplitude: confloat(ge=0.0, lt=10.0, multiple_of=0.01) = 5.0
    phase: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    offset: confloat(ge=-5.0, lt=5.0, multiple_of=0.01) = 0.0

    sigma: confloat(ge=0, le=3.0, multiple_of=0.01) = 1.0

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Frequency:').grid(row=0, column=0)
        self.ui_create_freq_mult(frm).grid(row=0, column=1)

        ttk.Label(frm, text='Amplitude:').grid(row=1, column=0)
        self.ui_create_amplitude(frm).grid(row=1, column=1)

        ttk.Label(frm, text='Phase:').grid(row=2, column=0)
        self.ui_create_phase(frm).grid(row=2, column=1)
        ttk.Label(frm, text='°').grid(row=2, column=2)

        ttk.Label(frm, text='Offset:').grid(row=3, column=0)
        self.ui_create_offset(frm).grid(row=3, column=1)

        ttk.Label(frm, text='Standard Deviation:').grid(row=4, column=0)
        self.ui_create_sigma(frm).grid(row=4, column=1)

        return frm

    def calc_signal(self, t: np.ndarray | int = 0) -> np.ndarray:
        phas = self.amplitude * np.exp(1j * self.phase * np.pi / 180)
        phi = np.exp(1j * 2 * np.pi * self.freq_mult * t)
        if type(t) == int:
            ran_vec = np.random.normal(self.offset, self.sigma)
        else:
            ran_vec = np.random.normal(self.offset, self.sigma, len(t))
        return (phas * phi) + ran_vec

    def make_title(self):
        return f'n={self.freq_mult}, {self.amplitude}, {self.phase}°, sigma={self.sigma}'


class ConfigCh03ErgodicFrame(ConfigControlFrame):
    wdg_seed: ttk.Spinbox
    wdg_funcs: Listbox


@ui_create
class ConfigCh03Ergodic(ConfigObject):
    _KEY = 'ch03_ergodic'

    random_seed: conint(ge=0, lt=10000) = 1000
    functions: List[Function] = [
        Function(),
        Function(),
        Function(),
        Function(),
        Function(),
        Function(),
    ]

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigCh03ErgodicFrame(parent, borderwidth=1, relief='raised')

        frm1 = ttk.Frame(frm)
        frm1.pack()

        ttk.Label(frm1, text='Random Seed:').grid(row=0, column=0)
        frm.wdg_seed = self.ui_create_random_seed(frm1)
        frm.wdg_seed.grid(row=0, column=1)

        ttk.Label(frm, text='Functions:').pack()
        frm.wdg_funcs = self.ui_create_functions_list(frm, lambda e: e.make_title())
        frm.wdg_funcs.pack()

        return frm


class Ch03ErgodicFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh03Ergodic = default_store().get_config(ConfigCh03Ergodic)

        ctrl_frm = self._create_control()
        ctrl_frm.pack(side=LEFT)

        signal_frm = self._create_signal_canvas()
        signal_frm.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigCh03ErgodicFrame:
        frm: ConfigCh03ErgodicFrame = self._config.make_config_widget(self)
        frm.wdg_seed.listen_change(self._on_change)
        frm.wdg_funcs.listen_change(self._on_change)
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

        np.random.seed(self._config.random_seed)

        self._signal_fig.clear()
        ax = self._signal_fig.add_subplot(1, 1, 1)
        ax.set_xlim(-1.2, 1.2)
        ax.set_xlabel('time')
        ax.set_ylabel('value')
        ax.set_title('Signal')

        t = np.linspace(-1.0, 1.0, LENGTH)

        x = np.zeros((len(self._config.functions), LENGTH))
        temp_mean = np.zeros((len(self._config.functions), ))
        for index, func in enumerate(self._config.functions):
            x[index, :] = func.calc_signal(t)
            temp_mean[index] = np.mean(x[index, :])

        stoch_mean = np.mean(x, axis=0)

        for index, func in enumerate(self._config.functions):
            ax.plot(t, x[index, :], label=f'{func.make_title()}', linestyle='solid', linewidth=1)
            ones = np.ones(len(t))
            ax.plot(t, ones*temp_mean[index], label=f'Temp. Mean {func.make_title()}', linestyle='solid', linewidth=2)
        ax.plot(t, stoch_mean, label='Stochastic Mean', linestyle='solid', linewidth=3)
        ax.legend()

        self._signal_canvas.draw()


class Ch03ErgodicWindow(Window):
    GROUP = Ch03Group
    TITLE = 'Ergodic Process'
    FRAME = Ch03ErgodicFrame


if __name__ == '__main__':
    Ch03ErgodicWindow.main()

