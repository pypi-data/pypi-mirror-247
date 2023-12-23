#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk, LEFT, BOTH, BOTTOM
from pydantic import confloat
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
import scipy.signal
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch06Group
from dcs.utils import swap_freq, abs_log_fft
from typing import List
from enum import Enum

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


SAMPLE_LEN = 512
FFT_OVERSAMPLING = 64


@ui_create
class Function(ConfigObject):
    freq: confloat(ge=-16*SAMPLE_LEN, lt=16*SAMPLE_LEN, multiple_of=(4.0/FFT_OVERSAMPLING)) = 1.0
    amplitude_dB: confloat(ge=-100.0, lt=10.0, multiple_of=1) = 0.0
    phase: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0
    offset: confloat(ge=-5.0, lt=5.0, multiple_of=0.01) = 0.0

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent)

        ttk.Label(frm, text='Frequency:').grid(row=0, column=0)
        w = self.ui_create_freq(frm)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        ttk.Label(frm, text='Amplitude:').grid(row=1, column=0)
        w = self.ui_create_amplitude_dB(frm)
        frm.add_widget(w)
        w.grid(row=1, column=1)
        ttk.Label(frm, text='dB').grid(row=1, column=2)

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

    def calc_signal(self, t: np.ndarray) -> np.ndarray:
        phasor = np.power(10, self.amplitude_dB / 20) * np.exp(1j * self.phase * np.pi / 180)
        phi = np.exp(1j * 2 * np.pi * self.freq * t)
        return self.offset + (phasor * phi)

    def make_title(self):
        return f'f={self.freq}, {self.amplitude_dB} dB, {self.phase}°'


class Direction(str, Enum):
    UP = 'Up Conversion'
    DOWN = 'Down Conversion'


@ui_create
class ConfigCh06Mixer(ConfigObject):
    _KEY = 'ch06_mixer'

    input_funcs: List[Function] = [
        Function(freq=-1.0, amplitude_dB=0.0, phase=0.0),
        Function(freq=2.0, amplitude_dB=0.0, phase=90.0),
    ]
    direction: Direction = Direction.UP
    nco: Function = Function(freq=20.0, amplitude_dB=0.0)

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Input Functions:').pack()
        w = self.ui_create_input_funcs_list(frm, lambda e: e.make_title())
        frm.add_widget(w)
        w.pack()

        frm1 = ttk.Frame(frm)
        frm1.pack()
        ttk.Label(frm1, text='Conversion Direction:').grid(row=0, column=0)
        w = self.ui_create_direction_dropdown(frm1)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        frm2 = ttk.Frame(frm, borderwidth=1, relief='raised')
        frm2.pack()
        ttk.Label(frm2, text='Carrier:').pack()
        carrier_frm = self.nco.make_config_widget(frm2)
        for w in carrier_frm.ctrl_widgets:
            frm.add_widget(w)
        carrier_frm.pack()

        return frm

    def calc_oscillator_signal(self, t: np.ndarray) -> np.ndarray:
        if self.direction == Direction.UP:
            return self.nco.calc_signal(t)
        elif self.direction == Direction.DOWN:
            return np.conjugate(self.nco.calc_signal(t))
        else:
            raise Exception('Invalid direction')

    def calc_input_signal(self, t: np.ndarray) -> np.ndarray:
        x = np.zeros((len(self.input_funcs), len(t)), dtype='complex128')
        for index, func in enumerate(self.input_funcs):
            x[index, :] = func.calc_signal(t)
        return np.sum(x, axis=0)

    def calc_output_signal(self, t: np.ndarray) -> np.ndarray:
        inp = self.calc_input_signal(t)
        carrier = self.calc_oscillator_signal(t)
        re_mixed = (np.real(inp) * np.real(carrier)) - (np.imag(inp) * np.imag(carrier))
        im_mixed = (np.imag(inp) * np.real(carrier)) + (np.real(inp) * np.imag(carrier))
        return re_mixed + (1j * im_mixed)


class Ch06MixerFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh06Mixer = default_store().get_config(ConfigCh06Mixer)

        ctrl_frm = self._create_control()
        ctrl_frm.pack(side=LEFT)

        signal_frm = self._create_signal_tabs()
        signal_frm.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigControlFrame:
        frm = self._config.make_config_widget(self)
        frm.widgets_on_change(self._on_change)
        return frm

    def _on_change(self, _, __, ___):
        default_store().save()
        self.draw_td()
        self.draw_fd()

    def _create_signal_tabs(self) -> ttk.Widget:
        tabs = ttk.Notebook(self)

        td_frm = ttk.Frame(tabs)
        tabs.add(td_frm, text='Time Domain')
        self._td_fig = Figure(figsize=(12, 6), dpi=100)
        self._td_canvas = FigureCanvasTkAgg(self._td_fig, td_frm)
        self._td_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        td_tb = NavigationToolbar2Tk(self._td_canvas, td_frm, pack_toolbar=False)
        td_tb.pack(side=BOTTOM)

        fd_frm = ttk.Frame(tabs)
        tabs.add(fd_frm, text='Frequency Domain')
        self._fd_fig = Figure(figsize=(12, 6), dpi=100)
        self._fd_canvas = FigureCanvasTkAgg(self._fd_fig, fd_frm)
        self._fd_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        fd_tb = NavigationToolbar2Tk(self._fd_canvas, fd_frm, pack_toolbar=False)
        fd_tb.pack(side=BOTTOM)

        self.draw_td()
        self.draw_fd()

        return tabs

    def draw_td(self):
        self._td_fig.clear()

        ax_inp = self._td_fig.add_subplot(3, 1, 1)
        ax_inp.set_xlim(0.0, 1.0)
        ax_inp.set_xlabel('time')
        ax_inp.set_ylabel('value')
        ax_inp.set_title('Input Signal')
        ax_nco = self._td_fig.add_subplot(3, 1, 2)
        ax_nco.set_xlim(0.0, 1.0)
        ax_nco.set_xlabel('time')
        ax_nco.set_ylabel('value')
        ax_nco.set_title('Numerically-Controlled Oscillator Signal')
        ax_out = self._td_fig.add_subplot(3, 1, 3)
        ax_out.set_xlim(0.0, 1.0)
        ax_out.set_xlabel('time')
        ax_out.set_ylabel('value')
        ax_out.set_title('Output Signal')

        t = np.arange(0, SAMPLE_LEN, 1) / SAMPLE_LEN

        x_inp = self._config.calc_input_signal(t)
        ax_inp.plot(t, np.real(x_inp), label='Input Re (I)', linestyle='solid', color='blue', linewidth=1)
        ax_inp.plot(t, np.imag(x_inp), label='Input Im (Q)', linestyle='solid', color='red', linewidth=1)
        ax_inp.legend()

        x_nco = self._config.calc_oscillator_signal(t)
        ax_nco.plot(t, np.real(x_nco), label='NCO Re (I)', linestyle='solid', color='green', linewidth=1)
        ax_nco.plot(t, np.imag(x_nco), label='NCO Im (Q)', linestyle='solid', color='orange', linewidth=1)
        ax_nco.legend()

        x_out = self._config.calc_output_signal(t)
        ax_out.plot(t, np.real(x_out), label='Output Re (I)', linestyle='solid', color='blue', linewidth=1)
        ax_out.plot(t, np.imag(x_out), label='Output Im (Q)', linestyle='solid', color='red', linewidth=1)
        ax_out.legend()

        self._td_fig.tight_layout()
        self._td_canvas.draw()

    @classmethod
    def _log_real(cls, x: np.ndarray) -> np.ndarray:
        return np.real(x)

    @classmethod
    def _log_imag(cls, x: np.ndarray) -> np.ndarray:
        return np.imag(x)

    @classmethod
    def _log_abs(cls, x: np.ndarray) -> np.ndarray:
        return np.abs(x)

    def draw_fd(self):
        self._fd_fig.clear()

        ax_inp = self._fd_fig.add_subplot(2, 1, 1)
        ax_inp.set_xlim(-int(SAMPLE_LEN/2), int(SAMPLE_LEN/2))
        ax_inp.set_xlabel('frequency')
        ax_inp.set_ylabel('value (dB)')
        ax_inp.set_title('Input Signals')
        ax_out = self._fd_fig.add_subplot(2, 1, 2)
        ax_out.set_xlim(-int(SAMPLE_LEN/2), int(SAMPLE_LEN/2))
        ax_out.set_xlabel('frequency')
        ax_out.set_ylabel('value (dB)')
        ax_out.set_title('Output Signal')

        t_ovs = np.arange(0, (SAMPLE_LEN * FFT_OVERSAMPLING), 1) / SAMPLE_LEN
        f_ovs = swap_freq(np.fft.fftfreq(t_ovs.shape[-1], 1.0/SAMPLE_LEN))

        x_inp = self._config.calc_input_signal(t_ovs)
        x_nco = self._config.calc_oscillator_signal(t_ovs)
        ax_inp.plot(f_ovs, abs_log_fft(x_inp), label='Input', linestyle='solid', color='blue', linewidth=1)
        ax_inp.plot(f_ovs, abs_log_fft(x_nco), label='NCO', linestyle='solid', color='green', linewidth=1)
        ax_inp.legend()

        x_out = self._config.calc_output_signal(t_ovs)
        ax_out.plot(f_ovs, abs_log_fft(x_out), label='Output', linestyle='solid', color='brown', linewidth=1)
        ax_out.legend()

        self._fd_fig.tight_layout()
        self._fd_canvas.draw()


class Ch06MixerWindow(Window):
    GROUP = Ch06Group
    TITLE = 'Digital Mixer'
    FRAME = Ch06MixerFrame


if __name__ == '__main__':
    Ch06MixerWindow.main()

