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
from dcs.frames.groups import Ch02Group
from typing import List

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ConfigCh02FourierFrame(ConfigControlFrame):
    wdg_abs_input: List[ttk.Spinbox]
    wdg_phas_input: List[ttk.Spinbox]


@ui_create
class ConfigCh02Fourier(ConfigObject):
    _KEY = 'ch02_fourier'

    n0_abs: confloat(ge=-5.0, le=5.0, multiple_of=0.01) = 0.0

    n1_abs: confloat(ge=0.0, le=5.0, multiple_of=0.01) = 1.0
    n1_phas: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    n2_abs: confloat(ge=0.0, le=5.0, multiple_of=0.01) = 0.0
    n2_phas: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    n3_abs: confloat(ge=0.0, le=5.0, multiple_of=0.01) = 0.0
    n3_phas: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    n4_abs: confloat(ge=0.0, le=5.0, multiple_of=0.01) = 0.0
    n4_phas: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    n5_abs: confloat(ge=0.0, le=5.0, multiple_of=0.01) = 0.0
    n5_phas: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    n6_abs: confloat(ge=0.0, le=5.0, multiple_of=0.01) = 0.0
    n6_phas: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    n7_abs: confloat(ge=0.0, le=5.0, multiple_of=0.01) = 0.0
    n7_phas: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    n8_abs: confloat(ge=0.0, le=5.0, multiple_of=0.01) = 0.0
    n8_phas: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    n9_abs: confloat(ge=0.0, le=5.0, multiple_of=0.01) = 0.0
    n9_phas: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    def calc_vec(self, n: int, t: np.ndarray | int = 0) -> complex:
        if n > 0:
            phas = getattr(self, f'n{n}_abs') * np.exp(1j * getattr(self, f'n{n}_phas') * np.pi / 180)
        else:
            phas = getattr(self, f'n{n}_abs')
        t = np.exp(1j * 2 * np.pi * n * t)
        return phas * t

    def ui_create_abs(self, n: int, frm):
        ui_create = getattr(self, f'ui_create_n{n}_abs')
        return ui_create(frm)

    def ui_create_phas(self, n: int, frm):
        ui_create = getattr(self, f'ui_create_n{n}_phas')
        return ui_create(frm)

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigCh02FourierFrame(parent, borderwidth=1, relief='raised')

        frm.wdg_abs_input = []
        frm.wdg_phas_input = []

        for idx in range(10):
            ttk.Label(frm, text=f'n = {idx}:').grid(row=idx, column=0)

            wdg_abs = self.ui_create_abs(idx, frm)
            wdg_abs.grid(row=idx, column=1)
            frm.wdg_abs_input.append(wdg_abs)

            if idx > 0:
                ttk.Label(frm, text='Phase:').grid(row=idx, column=2)

                wdg_phas = self.ui_create_phas(idx, frm)
                wdg_phas.grid(row=idx, column=3)
                frm.wdg_phas_input.append(wdg_phas)

                ttk.Label(frm, text='°').grid(row=idx, column=4)

        return frm


class Ch02FourierFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config = default_store().get_config(ConfigCh02Fourier)

        self.ctrl_frm = self._create_control()
        self.ctrl_frm.pack(side=LEFT)

        signal_frm = self._create_signal_canvas()
        signal_frm.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigCh02FourierFrame:
        frm = self._config.make_config_widget(self)
        for wdg in frm.wdg_abs_input:
            wdg.listen_change(self._on_change)
        for wdg in frm.wdg_phas_input:
            wdg.listen_change(self._on_change)
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

        self._signal_fig.clear()
        ax = self._signal_fig.add_subplot(1, 1, 1)
        ax.set_xlim(-1.2, 1.2)
        ax.set_xlabel('time')
        ax.set_ylabel('value')
        ax.set_title('Signal')

        t = np.linspace(-1.0, 1.0, LENGTH)

        x = np.zeros((10, LENGTH))
        for n in range(10):
            x[n, :] = self._config.calc_vec(n, t)

        s = np.sum(x, axis=0)

        ax.plot(t, s, label='Sum', linestyle='solid', linewidth=3)
        for n in range(10):
            ax.plot(t, x[n, :], label=f'n = {n}', linestyle='solid', linewidth=1)
        ax.legend()

        self._signal_canvas.draw()


class Ch02FourierWindow(Window):
    GROUP = Ch02Group
    TITLE = 'Fourier Series'
    FRAME = Ch02FourierFrame


if __name__ == '__main__':
    Ch02FourierWindow.main()

