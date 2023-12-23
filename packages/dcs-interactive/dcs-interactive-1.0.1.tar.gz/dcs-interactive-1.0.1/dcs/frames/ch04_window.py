#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk, Listbox, LEFT, BOTH
from pydantic import confloat
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
import scipy.signal.windows
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch04Group
from dcs.utils import swap_freq, abs_log_fft
from typing import List
from enum import Enum

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


LENGTH = 256
WINDOW_OVERSAMPLING = 64


@ui_create
class Function(ConfigObject):
    freq: confloat(ge=0.0, lt=128.0, multiple_of=0.01) = 1.0
    amplitude: confloat(ge=-100.0, lt=10.0, multiple_of=0.01) = 0.0
    phase: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Frequency:').grid(row=0, column=0)
        self.ui_create_freq(frm).grid(row=0, column=1)
        ttk.Label(frm, text=f'x sampling frequency / {LENGTH}').grid(row=0, column=2)

        ttk.Label(frm, text='Amplitude:').grid(row=1, column=0)
        self.ui_create_amplitude(frm).grid(row=1, column=1)
        ttk.Label(frm, text='dB').grid(row=1, column=2)

        ttk.Label(frm, text='Phase:').grid(row=2, column=0)
        self.ui_create_phase(frm).grid(row=2, column=1)
        ttk.Label(frm, text='°').grid(row=2, column=2)

        return frm

    def get_lin_amplitude(self) -> np.ndarray:
        return np.power(10, (self.amplitude / 20))

    def calc_signal(self, t: np.ndarray = 0) -> np.ndarray:
        phasor = self.get_lin_amplitude() * np.exp(1j * self.phase * np.pi / 180)
        phi = np.exp(1j * 2 * np.pi * self.freq * t)
        return np.real(phasor * phi)

    def make_title(self):
        return f'f={self.freq}, A={self.get_lin_amplitude()}={self.amplitude}dB'


class WindowFunc(str, Enum):
    Rectangular = 'Rectangular'
    Hamming = 'Hamming'
    Blackman = 'Blackman'
    Bartlett = 'Bartlett'
    Hann = 'Hann'
    Gaussian_025 = 'Gaussian (sigma = 0.25)'
    Gaussian_0125 = 'Gaussian (sigma = 0.125)'
    Gaussian_00625 = 'Gaussian (sigma = 0.0625)'


class ConfigCh04WindowFrame(ConfigControlFrame):
    wdg_funcs: Listbox
    wdg_window: ttk.OptionMenu
    wgd_win_sampling_delay: ttk.Spinbox


@ui_create
class ConfigCh04Window(ConfigObject):
    _KEY = 'ch04_window'

    functions: List[Function] = [
        Function(),
    ]
    window: WindowFunc = WindowFunc.Rectangular
    win_sampling_delay: confloat(ge=0.0, lt=1.0, multiple_of=0.01) = 0.25

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigCh04WindowFrame(parent, borderwidth=1, relief='raised')

        frm1 = ttk.Frame(frm)
        frm1.pack()

        ttk.Label(frm1, text='Window:').grid(row=0, column=0)
        frm.wdg_window = self.ui_create_window_dropdown(frm1)
        frm.wdg_window.grid(row=0, column=1)

        ttk.Label(frm1, text='Window Sampling Delay:').grid(row=1, column=0)
        frm.wgd_win_sampling_delay = self.ui_create_win_sampling_delay(frm1)
        frm.wgd_win_sampling_delay.grid(row=1, column=1)
        ttk.Label(frm1, text='x 360°').grid(row=1, column=2)

        ttk.Label(frm, text='Functions:').pack()
        frm.wdg_funcs = self.ui_create_functions_list(frm, lambda e: e.make_title())
        frm.wdg_funcs.pack()

        return frm


class Ch04WindowFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh04Window = default_store().get_config(ConfigCh04Window)

        ctrl_frm = self._create_control()
        ctrl_frm.pack(side=LEFT)

        signal_frm = self._create_signal_canvas()
        signal_frm.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigCh04Window:
        frm: ConfigCh04Window = self._config.make_config_widget(self)
        frm.wdg_funcs.listen_change(self._on_change)
        frm.wdg_window.listen_change(self._on_change)
        frm.wgd_win_sampling_delay.listen_change(self._on_change)
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
        ax_sig_td = self._signal_fig.add_subplot(2, 2, 1)
        ax_sig_td.set_xlim(-0.2, 1.2)
        ax_sig_td.set_xlabel('time')
        ax_sig_td.set_ylabel('value')
        ax_sig_td.set_title('Sampled Time-Domain Signal')
        ax_win_td = self._signal_fig.add_subplot(2, 2, 2)
        ax_win_td.set_xlim(-0.2, 1.2)
        ax_win_td.set_ylim(-0.2, 1.2)
        ax_win_td.set_xlabel('time')
        ax_win_td.set_ylabel('value')
        ax_win_td.set_title('Window Time-Domain')
        ax_sig_fd = self._signal_fig.add_subplot(2, 2, 3)
        ax_sig_fd.set_xlim(-int(LENGTH/4) - 1, int(LENGTH/4) + 1)
        ax_sig_fd.set_ylim(-120.0, 23.0)
        ax_sig_fd.set_xlabel('frequency')
        ax_sig_fd.set_ylabel('value (logarithmic)')
        ax_sig_fd.set_title('Frequency-Domain of Windowed Signal')
        ax_win_fd = self._signal_fig.add_subplot(2, 2, 4)
        ax_win_fd.set_xlim(-int(LENGTH/4) - 1, int(LENGTH/4) + 1)
        ax_win_fd.set_ylim(-180.0, 0.0)
        ax_win_fd.set_xlabel('frequency')
        ax_win_fd.set_ylabel('value (logarithmic)')
        ax_win_fd.set_title('Window Frequency-Domain')

        t = np.arange(0, LENGTH, 1) / LENGTH
        f = swap_freq(np.fft.fftfreq(t.shape[-1], 1.0/LENGTH))
        t_ovs = np.arange(0, LENGTH, (1/WINDOW_OVERSAMPLING)) / LENGTH
        f_win_ovs = swap_freq(np.fft.fftfreq(t_ovs.shape[-1], 1.0/LENGTH))
        f_sig_ovs = swap_freq(np.fft.fftfreq(t_ovs.shape[-1], 1.0/(LENGTH * WINDOW_OVERSAMPLING)))

        x = np.zeros((len(self._config.functions), len(t)))
        x_ovs = np.zeros((len(self._config.functions), len(t_ovs)))

        for index, func in enumerate(self._config.functions):
            x[index, :] = func.calc_signal(t)
            x_ovs[index, :] = func.calc_signal(t_ovs)
        func = np.sum(x, axis=0)
        func_ovs = np.sum(x_ovs, axis=0)

        func_ovs_fft = abs_log_fft(func_ovs)

        if self._config.window == WindowFunc.Rectangular:
            win = np.ones((len(t),))
        elif self._config.window == WindowFunc.Hamming:
            win = scipy.signal.windows.hamming(len(t))
        elif self._config.window == WindowFunc.Blackman:
            win = scipy.signal.windows.blackman(len(t))
        elif self._config.window == WindowFunc.Bartlett:
            win = scipy.signal.windows.bartlett(len(t))
        elif self._config.window == WindowFunc.Hann:
            win = scipy.signal.windows.hann(len(t))
        elif self._config.window == WindowFunc.Gaussian_025:
            win = scipy.signal.windows.gaussian(len(t), len(t)/4)
        elif self._config.window == WindowFunc.Gaussian_0125:
            win = scipy.signal.windows.gaussian(len(t), len(t)/8)
        elif self._config.window == WindowFunc.Gaussian_00625:
            win = scipy.signal.windows.gaussian(len(t), len(t)/16)
        else:
            raise Exception(f'Unsupported window')

        func_windowed = func * win

        win_ovs = np.zeros((LENGTH * WINDOW_OVERSAMPLING, ))
        start_idx = int(LENGTH * WINDOW_OVERSAMPLING / 2) - int(LENGTH / 2)
        for idx in range(len(t)):
            win_ovs[start_idx + idx] = win[idx] * WINDOW_OVERSAMPLING
            # win_ovs[idx * WINDOW_OVERSAMPLING] = win[idx]

        # win_fft = 20 * np.log10(np.abs(self._swap(np.fft.fft(win))) / len(win))
        win_ovs_fft = abs_log_fft(win_ovs)
        win_fft = np.zeros((len(win), ))
        win_180_fft = np.zeros((len(win), ))
        win_tau_fft = np.zeros((len(win), ))
        win_idx_delay = int(self._config.win_sampling_delay * WINDOW_OVERSAMPLING)
        win_phase_delay = np.round(360.0 * win_idx_delay / WINDOW_OVERSAMPLING)
        win_frac_delay = np.round(10000.0 * win_idx_delay / WINDOW_OVERSAMPLING) / 10000.0
        for idx in range(len(win)):
            win_fft[idx] = win_ovs_fft[idx * WINDOW_OVERSAMPLING]
            win_180_fft[idx] = win_ovs_fft[idx * WINDOW_OVERSAMPLING + int(WINDOW_OVERSAMPLING/2)]
            win_tau_fft[idx] = win_ovs_fft[idx * WINDOW_OVERSAMPLING + win_idx_delay]

        func_windowed_fft = abs_log_fft(func_windowed)

        ax_sig_td.plot(t, func, label='Time-Domain', linestyle='solid', linewidth=1)
        ax_sig_fd.plot(f, func_windowed_fft, label='Frequency-Domain Windows', linestyle='solid', linewidth=1)
        ax_win_td.plot(t, win, label='Time-Domain', linestyle='solid', linewidth=1)
        ax_win_fd.plot(f_win_ovs, win_ovs_fft, label='Window', linestyle='solid', linewidth=1)
        ax_win_fd.plot(f, win_fft, label='Window Sampled', linestyle='dashed', linewidth=1)
        ax_win_fd.plot(f, win_180_fft, label='Window Sampled (180° shift)', linestyle='dashed', linewidth=1)
        ax_win_fd.plot(f, win_tau_fft, label=f'Window Sampled ({win_frac_delay} x 360° = {win_phase_delay}° shift)', linestyle='dashed', linewidth=1)
        ax_win_fd.legend()

        self._signal_canvas.draw()


class Ch04WindowWindow(Window):
    GROUP = Ch04Group
    TITLE = 'Windowing'
    FRAME = Ch04WindowFrame


if __name__ == '__main__':
    Ch04WindowWindow.main()

