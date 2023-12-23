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
from dcs.frames.groups import Ch05Group
from dcs.utils import swap_freq
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
    freq: confloat(ge=-SAMPLE_LEN/4, lt=SAMPLE_LEN/4, multiple_of=(4.0/FFT_OVERSAMPLING)) = 1.0
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

    def calc_signal(self, t: np.ndarray) -> np.ndarray:
        phasor = self.amplitude * np.exp(1j * self.phase * np.pi / 180)
        phi = np.exp(1j * 2 * np.pi * self.freq * t)
        return self.offset + (phasor * phi)

    def make_title(self):
        return f'n={self.freq}, {self.amplitude}, {self.phase}°'


class Direction(str, Enum):
    DOWN = 'Down Conversion'
    UP = 'Up Conversion'


class DisplayMode(str, Enum):
    FULL = 'Full (I, Q, I+jQ)'
    IQ = 'IQ Channels (I, Q)'
    CMPLX = 'Complex (I+jQ)'
    BASEBAND = 'Baseband only'
    CARRIER = 'Carrier only'
    HF = 'HF only'


@ui_create
class ConfigCh05Iq(ConfigObject):
    _KEY = 'ch05_iq'

    hf_funcs: List[Function] = [
        Function(freq=-1.0, amplitude=1.0, phase=90.0),
        Function(freq=2.0, amplitude=1.0, phase=0.0),
    ]
    baseband_funcs: List[Function] = [
        Function(freq=18.0, amplitude=1.0, phase=0.0),
        Function(freq=21.0, amplitude=1.0, phase=90.0),
    ]
    direction: Direction = Direction.DOWN
    carrier: Function = Function(freq=20.0, amplitude=1.0)
    lp_cutoff_freq: confloat(ge=0, lt=SAMPLE_LEN/4, multiple_of=(4.0/FFT_OVERSAMPLING)) = 0.0
    display: DisplayMode = DisplayMode.FULL

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='HF Functions (for Down Conversion):').pack()
        w = self.ui_create_hf_funcs_list(frm, lambda e: e.make_title())
        frm.add_widget(w)
        w.pack()

        ttk.Label(frm, text='Baseband Functions (for Up Conversion):').pack()
        w = self.ui_create_baseband_funcs_list(frm, lambda e: e.make_title())
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
        carrier_frm = self.carrier.make_config_widget(frm2)
        for w in carrier_frm.ctrl_widgets:
            frm.add_widget(w)
        carrier_frm.pack()

        frm3 = ttk.Frame(frm)
        frm3.pack()
        ttk.Label(frm3, text='Down Conv. Baseband Low Pass Cut-off:').grid(row=0, column=0)
        ttk.Label(frm3, text='(0 = disable):').grid(row=1, column=1)
        w = self.ui_create_lp_cutoff_freq(frm3)
        frm.add_widget(w)
        w.grid(row=0, column=1)
        ttk.Label(frm3, text='Display Mode:').grid(row=2, column=0)
        w = self.ui_create_display_dropdown(frm3)
        frm.add_widget(w)
        w.grid(row=2, column=1)

        return frm

    def calc_carrier_signal(self, t: np.ndarray) -> np.ndarray:
        return self.carrier.calc_signal(t)

    def calc_baseband_signal(self, t: np.ndarray) -> np.ndarray:
        if self.direction == Direction.UP:
            x = np.zeros((len(self.baseband_funcs), len(t)), dtype='complex128')
            for index, func in enumerate(self.baseband_funcs):
                x[index, :] = func.calc_signal(t)
            return np.sum(x, axis=0)
        elif self.direction == Direction.DOWN:
            i_mixed = self.calc_hf_signal(t) * np.real(self.calc_carrier_signal(t))
            q_mixed = self.calc_hf_signal(t) * np.imag(self.calc_carrier_signal(t))
            base = i_mixed - (1j * q_mixed)

            if self.lp_cutoff_freq == 0:
                return base
            else:
                b, a = scipy.signal.butter(5, self.lp_cutoff_freq, btype='low', fs=SAMPLE_LEN)
                zi = scipy.signal.lfilter_zi(b, a)
                z, _ = scipy.signal.lfilter(b, a, base, zi=zi*base[0])
                return z
        else:
            raise Exception('Invalid direction')

    def calc_hf_signal(self, t: np.ndarray) -> np.ndarray:
        if self.direction == Direction.DOWN:
            x = np.zeros((len(self.hf_funcs), len(t)), dtype='float128')
            for index, func in enumerate(self.hf_funcs):
                x[index, :] = np.real(func.calc_signal(t))
            return np.sum(x, axis=0)
        elif self.direction == Direction.UP:
            i_mixed = np.real(self.calc_baseband_signal(t)) * np.real(self.calc_carrier_signal(t))
            q_mixed = np.imag(self.calc_baseband_signal(t)) * np.imag(self.calc_carrier_signal(t))
            return i_mixed - q_mixed
        else:
            raise Exception('Invalid direction')


class Ch05IqFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh05Iq = default_store().get_config(ConfigCh05Iq)

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
        self.draw_input()
        self.draw_fft()
        self.draw_output()

    def _create_signal_tabs(self) -> ttk.Widget:
        tabs = ttk.Notebook(self)

        in_frm = ttk.Frame(tabs)
        tabs.add(in_frm, text='Input Signals')
        self._in_fig = Figure(figsize=(12, 6), dpi=100)
        self._in_canvas = FigureCanvasTkAgg(self._in_fig, in_frm)
        self._in_canvas.get_tk_widget().pack(expand=True, fill=BOTH)

        fft_frm = ttk.Frame(tabs)
        tabs.add(fft_frm, text='Frequency Domain')
        self._fft_fig = Figure(figsize=(12, 6), dpi=100)
        self._fft_canvas = FigureCanvasTkAgg(self._fft_fig, fft_frm)
        self._fft_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        fft_tb = NavigationToolbar2Tk(self._fft_canvas, fft_frm, pack_toolbar=False)
        fft_tb.pack(side=BOTTOM)

        out_frm = ttk.Frame(tabs)
        tabs.add(out_frm, text='Output Signals')
        self._out_fig = Figure(figsize=(12, 6), dpi=100)
        self._out_canvas = FigureCanvasTkAgg(self._out_fig, out_frm)
        self._out_canvas.get_tk_widget().pack(expand=True, fill=BOTH)

        self.draw_input()
        self.draw_fft()
        self.draw_output()

        return tabs

    def draw_input(self):
        self._in_fig.clear()

        ax_inp = self._in_fig.add_subplot(3, 1, 1)
        ax_inp.set_xlim(0.0, 1.0)
        ax_inp.set_xlabel('time')
        ax_inp.set_ylabel('value')
        ax_inp.set_title('Baseband Signal' if self._config.direction == Direction.UP else 'HF Signal')
        ax_carr = self._in_fig.add_subplot(3, 1, 2)
        ax_carr.set_xlim(0.0, 1.0)
        ax_carr.set_xlabel('time')
        ax_carr.set_ylabel('value')
        ax_carr.set_title('Carrier Signal')
        ax_3d = self._in_fig.add_subplot(3, 1, 3, projection='3d')
        ax_3d.set_xlabel('real')
        ax_3d.set_ylabel('imaginary')
        ax_3d.set_zlabel('time')

        t = np.arange(0, SAMPLE_LEN, 1) / SAMPLE_LEN

        if self._config.direction == Direction.UP:
            x_base = self._config.calc_baseband_signal(t)
            ax_inp.plot(t, np.real(x_base), label='Baseband I', linestyle='solid', color='blue', linewidth=1)
            ax_inp.plot(t, np.imag(x_base), label='Baseband Q', linestyle='solid', color='red', linewidth=1)
            ax_3d.plot(np.real(x_base), np.imag(x_base), t, label='Baseband', linestyle='solid', color='purple', linewidth=1)
        elif self._config.direction == Direction.DOWN:
            x_hf = self._config.calc_hf_signal(t)
            ax_inp.plot(t, x_hf, label='HF', linestyle='solid', color='brown', linewidth=1)
            ax_3d.plot(x_hf, np.zeros(len(x_hf)), t, label='HF', linestyle='solid', color='brown', linewidth=1)
        else:
            raise Exception('Invalid direction')
        ax_inp.legend()

        x_carr = self._config.calc_carrier_signal(t)
        ax_carr.plot(t, np.real(x_carr), label='Carrier I', linestyle='solid', color='green', linewidth=1)
        ax_carr.plot(t, np.imag(x_carr), label='Carrier Q', linestyle='solid', color='orange', linewidth=1)
        ax_carr.legend()

        ax_3d.plot(np.real(x_carr), np.imag(x_carr), t, label='Carrier', linestyle='solid', color='yellow', linewidth=1)
        ax_3d.legend()

        self._in_fig.tight_layout()
        self._in_canvas.draw()

    @classmethod
    def _log_real(cls, x: np.ndarray) -> np.ndarray:
        return np.real(x)

    @classmethod
    def _log_imag(cls, x: np.ndarray) -> np.ndarray:
        return np.imag(x)

    @classmethod
    def _log_abs(cls, x: np.ndarray) -> np.ndarray:
        return np.abs(x)

    def draw_fft(self):
        self._fft_fig.clear()

        # ax_3d = self._fft_fig.add_subplot(3, 1, 1, projection='3d')
        # ax_3d.set_zlim(-int(SAMPLE_LEN/4), int(SAMPLE_LEN/4))
        # ax_3d.set_xlabel('real')
        # ax_3d.set_ylabel('imag')
        # ax_3d.set_zlabel('frequency')
        #ax_real = self._fft_fig.add_subplot(3, 1, 2)
        ax_real = self._fft_fig.add_subplot(2, 1, 1)
        ax_real.set_xlim(-int(SAMPLE_LEN/4), int(SAMPLE_LEN/4))
        ax_real.set_xlabel('frequency')
        ax_real.set_ylabel('value')
        ax_real.set_title('Real(FFT)')
        #ax_imag = self._fft_fig.add_subplot(3, 1, 3)
        ax_imag = self._fft_fig.add_subplot(2, 1, 2)
        ax_imag.set_xlim(-int(SAMPLE_LEN/4), int(SAMPLE_LEN/4))
        ax_imag.set_xlabel('frequency')
        ax_imag.set_ylabel('value')
        ax_imag.set_title('Imag(FFT)')

        t_ovs = np.arange(0, (SAMPLE_LEN * FFT_OVERSAMPLING), 1) / SAMPLE_LEN
        f_ovs = swap_freq(np.fft.fftfreq(t_ovs.shape[-1], 1.0/SAMPLE_LEN))

        x_base = self._config.calc_baseband_signal(t_ovs)
        X_base_i = swap_freq(np.fft.fft(np.real(x_base))) / len(t_ovs)
        X_base_q = swap_freq(np.fft.fft(np.imag(x_base))) / len(t_ovs)
        X_base_cmplx = swap_freq(np.fft.fft(x_base)) / len(t_ovs)
        if (self._config.display == DisplayMode.FULL) or (self._config.display == DisplayMode.IQ) or (self._config.display == DisplayMode.BASEBAND):
            ax_real.plot(f_ovs, np.real(X_base_i), label='Baseband I', linestyle='solid', color='blue', marker='x', linewidth=1)
            ax_imag.plot(f_ovs, np.imag(X_base_i), label='Baseband I', linestyle='solid', color='blue', marker='x', linewidth=1)
            #ax_3d.plot(np.real(X_base_i), np.imag(X_base_i), f_ovs, label='Baseband I', linestyle='solid', color='blue', marker='x', linewidth=1)
            ax_real.plot(f_ovs, np.real(X_base_q), label='Baseband Q', linestyle='solid', color='red', marker='o', linewidth=1)
            ax_imag.plot(f_ovs, np.imag(X_base_q), label='Baseband Q', linestyle='solid', color='red', marker='o', linewidth=1)
            #ax_3d.plot(np.real(X_base_q), np.imag(X_base_q), f_ovs, label='Baseband Q', linestyle='solid', color='red', marker='o', linewidth=1)
        if (self._config.display == DisplayMode.FULL) or (self._config.display == DisplayMode.CMPLX) or (self._config.display == DisplayMode.BASEBAND):
            ax_real.plot(f_ovs, np.real(X_base_cmplx), label='Baseband I + j*Q', linestyle='solid', color='purple', marker='^', linewidth=1)
            ax_imag.plot(f_ovs, np.imag(X_base_cmplx), label='Baseband I + j*Q', linestyle='solid', color='purple', marker='^', linewidth=1)
            #ax_3d.plot(np.real(X_base_cmplx), np.imag(X_base_cmplx), f_ovs, label='Baseband I + j*Q', linestyle='solid', color='purple', marker='^', linewidth=1)

        x_carr = self._config.calc_carrier_signal(t_ovs)
        X_carr_i = swap_freq(np.fft.fft(np.real(x_carr))) / len(t_ovs)
        X_carr_q = swap_freq(np.fft.fft(np.imag(x_carr))) / len(t_ovs)
        X_carr_cmplx = swap_freq(np.fft.fft(x_carr)) / len(t_ovs)
        if (self._config.display == DisplayMode.FULL) or (self._config.display == DisplayMode.IQ) or (self._config.display == DisplayMode.CARRIER):
            ax_real.plot(f_ovs, np.real(X_carr_i), label='Carrier I', linestyle='solid', color='green', marker='x', linewidth=1)
            ax_imag.plot(f_ovs, np.imag(X_carr_i), label='Carrier I', linestyle='solid', color='green', marker='x', linewidth=1)
            #ax_3d.plot(np.real(X_carr_i), np.imag(X_carr_i), f_ovs, label='Baseband I', linestyle='solid', color='green', marker='x', linewidth=1)
            ax_real.plot(f_ovs, np.real(X_carr_q), label='Carrier Q', linestyle='solid', color='orange', marker='o', linewidth=1)
            ax_imag.plot(f_ovs, np.imag(X_carr_q), label='Carrier Q', linestyle='solid', color='orange', marker='o', linewidth=1)
            #ax_3d.plot(np.real(X_carr_q), np.imag(X_carr_q), f_ovs, label='Baseband Q', linestyle='solid', color='orange', marker='o', linewidth=1)
        if (self._config.display == DisplayMode.FULL) or (self._config.display == DisplayMode.CMPLX) or (self._config.display == DisplayMode.CARRIER):
            ax_real.plot(f_ovs, np.real(X_carr_cmplx), label='Carrier I + j*Q', linestyle='solid', color='yellow', marker='^', linewidth=1)
            ax_imag.plot(f_ovs, np.imag(X_carr_cmplx), label='Carrier I + j*Q', linestyle='solid', color='yellow', marker='^', linewidth=1)
            #ax_3d.plot(np.real(X_carr_cmplx), np.imag(X_carr_cmplx), f_ovs, label='Carrier I + j*Q', linestyle='solid', color='yellow', marker='^', linewidth=1)

        x_hf = self._config.calc_hf_signal(t_ovs)
        X_hf_cmplx = swap_freq(np.fft.fft(x_hf)) / len(t_ovs)
        if (self._config.display != DisplayMode.BASEBAND) and (self._config.display != DisplayMode.CARRIER):
            ax_real.plot(f_ovs, np.real(X_hf_cmplx), label='HF', linestyle='solid', color='brown', marker='^', linewidth=1)
            ax_imag.plot(f_ovs, np.imag(X_hf_cmplx), label='HF', linestyle='solid', color='brown', marker='^', linewidth=1)
            #ax_3d.plot(np.real(X_hf_cmplx), np.imag(X_hf_cmplx), f_ovs, label='HF', linestyle='solid', color='brown', linewidth=1)

        #ax_3d.legend()
        ax_real.legend()
        ax_imag.legend()

        self._fft_fig.tight_layout()
        self._fft_canvas.draw()

    def draw_output(self):
        self._out_fig.clear()

        ax_outp = self._out_fig.add_subplot(2, 1, 1)
        ax_outp.set_xlim(0.0, 1.0)
        ax_outp.set_xlabel('time')
        ax_outp.set_ylabel('value')
        ax_outp.set_title('HF Signal' if self._config.direction == Direction.UP else 'Baseband Signal')
        ax_3d = self._out_fig.add_subplot(2, 1, 2, projection='3d')
        ax_3d.set_xlabel('real')
        ax_3d.set_ylabel('imaginary')
        ax_3d.set_zlabel('time')

        t = np.arange(0, SAMPLE_LEN, 1) / SAMPLE_LEN

        if self._config.direction == Direction.UP:
            x_hf = self._config.calc_hf_signal(t)
            ax_outp.plot(t, x_hf, label='HF', linestyle='solid', color='brown', linewidth=1)
            ax_3d.plot(x_hf, np.zeros(len(x_hf)), t, label='HF', linestyle='solid', color='brown', linewidth=1)
        elif self._config.direction == Direction.DOWN:
            x_base = self._config.calc_baseband_signal(t)
            ax_outp.plot(t, np.real(x_base), label='Baseband I', linestyle='solid', color='blue', linewidth=1)
            ax_outp.plot(t, np.imag(x_base), label='Baseband Q', linestyle='solid', color='red', linewidth=1)
            ax_3d.plot(np.real(x_base), np.imag(x_base), t, label='Baseband', linestyle='solid', color='purple', linewidth=1)
        else:
            raise Exception('Invalid direction')
        ax_outp.legend()
        ax_3d.legend()

        self._out_fig.tight_layout()
        self._out_canvas.draw()


class Ch05IqWindow(Window):
    GROUP = Ch05Group
    TITLE = 'IQ Mixer'
    FRAME = Ch05IqFrame


if __name__ == '__main__':
    Ch05IqWindow.main()

