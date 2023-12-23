#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk, LEFT, BOTH, BOTTOM
from pydantic import confloat, conint
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
import scipy.signal
from scipy.interpolate import make_interp_spline
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch06Group
from dcs.utils import swap_freq, abs_log_fft
from typing import List, Tuple

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


OVERSAMPLING_LEN = 512
FFT_LEN = 2048


@ui_create
class Function(ConfigObject):
    freq: confloat(ge=0, lt=OVERSAMPLING_LEN/2, multiple_of=(4.0/OVERSAMPLING_LEN)) = 1.0
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
        return np.real(self.offset + (phasor * phi))

    def make_title(self):
        return f'f={self.freq}, {self.amplitude}, {self.phase}°'


@ui_create
class ConfigCh06UpSampling(ConfigObject):
    _KEY = 'ch06_up_sampling'

    input_funcs: List[Function] = [
        Function(freq=1.0, amplitude_dB=0.0, phase=0.0),
        Function(freq=1.5, amplitude_dB=0.0, phase=90.0),
    ]
    sample_rate: confloat(ge=0, lt=OVERSAMPLING_LEN/2, multiple_of=(4.0/OVERSAMPLING_LEN)) = 16.0
    interpolation: conint(ge=0, lt=64) = 4
    lp_cutoff_freq: confloat(ge=0, lt=OVERSAMPLING_LEN/2, multiple_of=(4.0/OVERSAMPLING_LEN)) = 4.0

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Input Functions:').pack()
        w = self.ui_create_input_funcs_list(frm, lambda e: e.make_title())
        frm.add_widget(w)
        w.pack()

        frm1 = ttk.Frame(frm, borderwidth=1, relief='raised')
        frm1.pack()

        ttk.Label(frm1, text='Sample Rate:').grid(row=0, column=0)
        w = self.ui_create_sample_rate(frm1)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        ttk.Label(frm1, text='Interpolation Factor:').grid(row=1, column=0)
        w = self.ui_create_interpolation(frm1)
        frm.add_widget(w)
        w.grid(row=1, column=1)

        ttk.Label(frm1, text='Interpolation Low Pass Cut-off:').grid(row=2, column=0)
        ttk.Label(frm1, text='(0 = disable):').grid(row=3, column=1)
        w = self.ui_create_lp_cutoff_freq(frm1)
        frm.add_widget(w)
        w.grid(row=2, column=1)

        return frm

    def have_filter(self) -> bool:
        return not (self.lp_cutoff_freq == 0)

    def calc_input_signal(self, t: np.ndarray) -> np.ndarray:
        x = np.zeros((len(self.input_funcs), len(t)), dtype=np.float64)
        for index, func in enumerate(self.input_funcs):
            x[index, :] = func.calc_signal(t)
        return np.sum(x, axis=0)

    def calc_zerofilled_signal(self, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        slope = (np.max(t) - np.min(t)) / (len(t) - 1)
        n_start = np.min(t) / slope
        n_up = len(t) * self.interpolation
        t_up = np.arange(n_start, n_start + n_up, 1) * slope / self.interpolation
        sig = np.zeros((n_up,))
        for idx, val in enumerate(self.calc_input_signal(t)):
            sig[idx * self.interpolation] = val
        return t_up, sig

    def calc_filtered_signal(self, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        t_up, zero_filled = self.calc_zerofilled_signal(t)

        if self.have_filter():
            b, a = scipy.signal.cheby1(N=5, Wn=self.lp_cutoff_freq, rp=1, btype='low', fs=self.sample_rate * self.interpolation)
            zi = scipy.signal.lfilter_zi(b, a)
            z, _ = scipy.signal.lfilter(b, a, zero_filled, zi=zi*zero_filled[0])
            return t_up, z
        else:
            return t_up, zero_filled


class Ch06UpSamplingFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh06UpSampling = default_store().get_config(ConfigCh06UpSampling)

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

        if self._config.have_filter():
            ax_inp = self._td_fig.add_subplot(3, 1, 1)
            ax_zer = self._td_fig.add_subplot(3, 1, 2)
            ax_int = self._td_fig.add_subplot(3, 1, 3)
        else:
            ax_inp = self._td_fig.add_subplot(2, 1, 1)
            ax_zer = self._td_fig.add_subplot(2, 1, 2)
        ax_inp.set_xlim(0.0, 1.1)
        ax_inp.set_xlabel('time')
        ax_inp.set_ylabel('value')
        ax_inp.set_title('Input Signal')
        ax_zer.set_xlim(0.0, 1.1)
        ax_zer.set_xlabel('time')
        ax_zer.set_ylabel('value')
        ax_zer.set_title('Zero-Filled Filter')
        if self._config.have_filter():
            ax_int.set_xlim(0.0, 1.1)
            ax_int.set_xlabel('time')
            ax_int.set_ylabel('value')
            ax_int.set_title('Interpolated Signal')

        t = np.arange(0, 1.1, 1.0/self._config.sample_rate)
        if len(t) > 3:
            t_interp = np.linspace(np.min(t), np.max(t), OVERSAMPLING_LEN)
        else:
            t_interp = np.zeros((0,))

        x_inp = self._config.calc_input_signal(t)
        if len(t) > 3:
            fn_inp_interp = make_interp_spline(t, x_inp)
            x_inp_interp = fn_inp_interp(t_interp)
        else:
            x_inp_interp = np.zeros((0,))

        t_zer, x_zer = self._config.calc_zerofilled_signal(t)
        if len(t) > 3:
            fn_zer_interp = make_interp_spline(t_zer, x_zer)
            x_zer_interp = fn_zer_interp(t_interp)
        else:
            x_zer_interp = np.zeros((0,))

        if self._config.have_filter():
            t_int, x_int = self._config.calc_filtered_signal(t)
            if len(t) > 3:
                fn_int_interp = make_interp_spline(t_int, x_int)
                x_int_interp = fn_int_interp(t_interp)
            else:
                x_int_interp = np.zeros((0,))

        ax_inp.plot(t, x_inp, label='Input Signal (Sampled)', marker='x', linestyle='none', color='blue', linewidth=1)
        ax_inp.plot(t_interp, x_inp_interp, label='Input Signal (Interpolated)', linestyle='dashed', color='blue', linewidth=1)
        ax_inp.legend()

        ax_zer.plot(t, x_inp, label='Input Signal (Sampled)', marker='o', linestyle='none', color='blue', linewidth=1)
        ax_zer.plot(t_zer, x_zer, label='Zero-Filled Signal (Sampled)', marker='x', linestyle='none', color='green', linewidth=1)
        ax_zer.plot(t_interp, x_zer_interp, label='Zero-Filled Signal (Interpolated)', linestyle='dashed', color='green', linewidth=1)
        ax_zer.legend()

        if self._config.have_filter():
            ax_int.plot(t_int, x_int, label='Interpolated Signal (Sampled)', marker='x', linestyle='none', color='red', linewidth=1)
            ax_int.plot(t_interp, x_int_interp, label='Interpolated Signal (Interpolated)', linestyle='dashed', color='red', linewidth=1)
            ax_int.legend()

        self._td_fig.tight_layout()
        self._td_canvas.draw()

    def draw_fd(self):
        self._fd_fig.clear()

        if self._config.have_filter():
            ax_inp = self._fd_fig.add_subplot(3, 1, 1)
            ax_zer = self._fd_fig.add_subplot(3, 1, 2)
            ax_int = self._fd_fig.add_subplot(3, 1, 3)
        else:
            ax_inp = self._fd_fig.add_subplot(2, 1, 1)
            ax_zer = self._fd_fig.add_subplot(2, 1, 2)
        ax_inp.set_xlim(-self._config.sample_rate/2, self._config.sample_rate/2)
        ax_inp.set_xlabel('frequency')
        ax_inp.set_ylabel('value (dB)')
        ax_inp.set_title('Input Signal')
        ax_zer.set_xlim(-self._config.interpolation * self._config.sample_rate/2, self._config.interpolation * self._config.sample_rate/2)
        ax_zer.set_xlabel('frequency')
        ax_zer.set_ylabel('value (dB)')
        ax_zer.set_title('Zero-Filled Filter')
        if self._config.have_filter():
            ax_int.set_xlim(-self._config.interpolation * self._config.sample_rate/2, self._config.interpolation * self._config.sample_rate/2)
            ax_int.set_xlabel('frequency')
            ax_int.set_ylabel('value (dB)')
            ax_int.set_title('Interpolated Signal')

        t = np.arange(0, FFT_LEN, 1) / self._config.sample_rate
        f = swap_freq(np.fft.fftfreq(t.shape[-1], 1.0/self._config.sample_rate))

        x_inp = self._config.calc_input_signal(t)
        t_zer, x_zer = self._config.calc_zerofilled_signal(t)
        f_zer = swap_freq(np.fft.fftfreq(t_zer.shape[-1], 1.0 / (self._config.sample_rate * self._config.interpolation)))

        if self._config.have_filter():
            t_int, x_int = self._config.calc_filtered_signal(t)
            f_int = swap_freq(np.fft.fftfreq(t_int.shape[-1], 1.0 / (self._config.sample_rate * self._config.interpolation)))

        ax_inp.plot(f, abs_log_fft(x_inp), label='Input Signal', linestyle='solid', color='blue', linewidth=1)
        ax_inp.legend()

        ax_zer.plot(f_zer, abs_log_fft(x_zer), label='Zero-Filled Signal', linestyle='solid', color='green', linewidth=1)
        ax_zer.legend()

        if self._config.have_filter():
            ax_int.plot(f_int, abs_log_fft(x_int), label='Interpolated Signal', linestyle='solid', color='red', linewidth=1)
            ax_int.legend()

        self._fd_fig.tight_layout()
        self._fd_canvas.draw()


class Ch06UpSamplingWindow(Window):
    GROUP = Ch06Group
    TITLE = 'Up Sampling'
    FRAME = Ch06UpSamplingFrame


if __name__ == '__main__':
    Ch06UpSamplingWindow.main()

