#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk, LEFT, X, BOTH
from tkinter.constants import DISABLED, NORMAL
from pydantic import conint, confloat
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
import threading
import time
from typing import Optional
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch02Group

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pyplot import Circle, Arrow
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ConfigCh02PhasorFrame(ConfigControlFrame):
    frm1: ttk.Frame
    wdg_real_input: ttk.Spinbox
    wdg_imag_input: ttk.Spinbox
    frm2: ttk.Frame
    wdg_freq_input: ttk.Spinbox


@ui_create
class ConfigCh02Phasor(ConfigObject):
    _KEY = 'ch02_phasor'

    real: confloat(ge=-5.0, lt=5.0, multiple_of=0.1) = 2.0
    imag: confloat(ge=-5.0, lt=5.0, multiple_of=0.1) = 0.0

    freq: conint(ge=0, lt=5) = 1

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigCh02PhasorFrame(parent)
        frm.frm1 = ttk.Frame(frm, borderwidth=1, relief='raised')
        frm.frm1.pack()
        frm.frm2 = ttk.Frame(frm, borderwidth=1, relief='raised')
        frm.frm2.pack()

        ttk.Label(frm.frm1, text='Real:').grid(row=0, column=0)
        frm.wdg_real_input = self.ui_create_real(frm.frm1)
        frm.wdg_real_input.grid(row=0, column=1)

        ttk.Label(frm.frm1, text='Imag:').grid(row=1, column=0)
        frm.wdg_imag_input = self.ui_create_imag(frm.frm1)
        frm.wdg_imag_input.grid(row=1, column=1)

        ttk.Label(frm.frm2, text='Frequency:').grid(row=0, column=0)
        frm.wdg_freq_input = self.ui_create_freq(frm.frm2)
        frm.wdg_freq_input.grid(row=0, column=1)

        return frm


class SimThread(threading.Thread):
    def __init__(self, ch01_frm: ConfigCh02PhasorFrame):
        super().__init__()
        self.ch01_frm = ch01_frm

    def run(self):
        t_max = 5
        n = 100
        for ctr in range(n):
            self.ch01_frm.draw_phasor(ctr, n)
            self.ch01_frm.draw_signal(ctr, n)
            time.sleep(t_max / n)
        self.ch01_frm.wdg_start_btn['state'] = NORMAL


class Ch02PhasorFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config = default_store().get_config(ConfigCh02Phasor)

        self.ctrl_frm = self._create_control()
        self.ctrl_frm.pack(side=LEFT)

        phasor_frm = self._create_phasor_canvas()
        phasor_frm.pack(fill=X)

        signal_frm = self._create_signal_canvas()
        signal_frm.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigCh02PhasorFrame:
        frm = self._config.make_config_widget(self)

        frm.wdg_real_input.listen_change(self._on_change)
        frm.wdg_imag_input.listen_change(self._on_change)

        ttk.Label(frm.frm1, text='Absolute:').grid(row=2, column=0)
        self.wdg_abs_output = ttk.Label(frm.frm1)
        self.wdg_abs_output.grid(row=2, column=1)

        ttk.Label(frm.frm1, text='Angle:').grid(row=3, column=0)
        self.wdg_angle_output = ttk.Label(frm.frm1)
        self.wdg_angle_output.grid(row=3, column=1)

        self.wdg_start_btn = ttk.Button(frm.frm2, text='Start', command=self._on_start)
        self.wdg_start_btn.grid(row=1, column=1)

        return frm

    def _on_change(self, _, __, ___):
        default_store().save()
        self.draw_phasor()

    def _on_start(self):
        default_store().save()
        self.wdg_start_btn['state'] = DISABLED
        self._thread = SimThread(self)
        self._thread.start()

    def _calc_sim_val(self, idx: int | np.ndarray, n: int) -> np.ndarray:
        phas = self._config.real + 1j * self._config.imag
        t = np.exp(1j * 2 * np.pi * self._config.freq * idx / n)
        return phas * t

    def _create_phasor_canvas(self) -> ttk.Widget:
        frm = ttk.Frame(self)

        self._phasor_fig = Figure(figsize=(5, 4), dpi=100)

        self._phasor_canvas = FigureCanvasTkAgg(self._phasor_fig, frm)
        self._phasor_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        self._phasor_canvas.mpl_connect('button_press_event', self._on_click_phasor)

        self.draw_phasor()

        return frm

    def draw_phasor(self, idx: Optional[int] = None, n: Optional[int] = None):
        num = self._calc_sim_val(0, 1)

        self.wdg_abs_output.configure(text=str(np.abs(num)))
        self.wdg_angle_output.configure(text=str(np.angle(num) * 180 / np.pi) + ' °')

        self._phasor_fig.clear()
        ax = self._phasor_fig.add_subplot(1, 1, 1)
        ax.set_xlim(-5.0, 5.0)
        ax.set_ylim(-5.0, 5.0)
        ax.set_xlabel('real')
        ax.set_ylabel('imag')

        ax.add_artist(Circle((0, 0), np.abs(num), fill=None))
        ax.add_artist(Arrow(0, 0, self._config.real, self._config.imag, label='Phasor'))
        ax.plot(self._config.real, self._config.imag, color='blue', marker='*')

        if idx is not None and n is not None:
            x = self._calc_sim_val(idx, n)
            ax.add_artist(Arrow(0, 0, x.real, x.imag, color='green', label='Current'))
            ax.add_artist(Arrow(0, 0, x.real, 0, color='red', label='Current real'))

        ax.legend()

        self._phasor_canvas.draw()

    def _on_click_phasor(self, ev):
        if ev.xdata is not None:
            self._config.real = np.round(10 * ev.xdata) / 10.
            self.ctrl_frm.wdg_real_input.sync_in()
        if ev.ydata is not None:
            self._config.imag = np.round(10 * ev.ydata) / 10.
            self.ctrl_frm.wdg_imag_input.sync_in()

        default_store().save()
        self.draw_phasor()

    def _create_signal_canvas(self) -> ttk.Widget:
        frm = ttk.Frame(self)

        self._signal_fig = Figure(figsize=(5, 4), dpi=100)

        self._signal_canvas = FigureCanvasTkAgg(self._signal_fig, frm)
        self._signal_canvas.get_tk_widget().pack(expand=True, fill=BOTH)

        return frm

    def draw_signal(self, idx: int, n: int):
        self._signal_fig.clear()
        ax = self._signal_fig.add_subplot(1, 1, 1)
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(-5.0, 5.0)
        ax.set_xlabel('time')
        ax.set_ylabel('value')
        ax.set_title('Signal')

        t = np.linspace(0.0, 1.0, n)
        t = t[:idx]

        x = self._calc_sim_val(np.arange(idx), n)

        ax.plot(t, x.real, color='red')

        self._signal_canvas.draw()


class Ch02PhasorWindow(Window):
    GROUP = Ch02Group
    TITLE = 'Phasor'
    FRAME = Ch02PhasorFrame


if __name__ == '__main__':
    Ch02PhasorWindow.main()

