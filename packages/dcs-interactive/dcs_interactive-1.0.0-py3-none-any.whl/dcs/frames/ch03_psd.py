#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk, LEFT, BOTH

import scipy.signal.windows
from pydantic import confloat, conint
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch03Group
from dcs.utils import swap_freq
from typing import List
from enum import Enum

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ConfigCh03PsdFrame(ConfigControlFrame):
    wdg_signal_rms: ttk.Label
    wdg_noise_rms: ttk.Label


class DisplayMode(str, Enum):
    Lin = 'linear'
    Log = 'logarithmic'


@ui_create
class ConfigCh03Psd(ConfigObject):
    _KEY = 'ch03_psd'

    amplitude_dBV: confloat(ge=-160.0, lt=40.0, multiple_of=0.1) = 5.0
    freq_mult: conint(ge=0, lt=32) = 16
    noise_dBV: confloat(ge=-160.0, le=40.0, multiple_of=0.1) = -10.0
    random_seed: conint(ge=0, lt=10000) = 1000

    disp_mode: DisplayMode = DisplayMode.Log

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigCh03PsdFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Signal Level:').grid(row=0, column=0)
        w = self.ui_create_amplitude_dBV(frm)
        w.grid(row=0, column=1)
        frm.add_widget(w)
        ttk.Label(frm, text='dBV').grid(row=0, column=2)

        ttk.Label(frm, text='Signal RMS:').grid(row=1, column=0)
        frm.wdg_signal_rms = ttk.Label(frm, text='')
        frm.wdg_signal_rms.grid(row=1, column=1)
        ttk.Label(frm, text='V').grid(row=1, column=2)

        ttk.Label(frm, text='Frequency:').grid(row=2, column=0)
        w = self.ui_create_freq_mult(frm)
        w.grid(row=2, column=1)
        frm.add_widget(w)

        ttk.Label(frm, text='Noise Level:').grid(row=3, column=0)
        w = self.ui_create_noise_dBV(frm)
        w.grid(row=3, column=1)
        frm.add_widget(w)
        ttk.Label(frm, text='dBV').grid(row=3, column=2)

        ttk.Label(frm, text='Noise RMS:').grid(row=4, column=0)
        frm.wdg_noise_rms = ttk.Label(frm, text='')
        frm.wdg_noise_rms.grid(row=4, column=1)
        ttk.Label(frm, text='V').grid(row=4, column=2)

        ttk.Label(frm, text='Random Seed:').grid(row=5, column=0)
        w = self.ui_create_random_seed(frm)
        w.grid(row=5, column=1)
        frm.add_widget(w)

        ttk.Label(frm, text='Display Mode:').grid(row=6, column=0)
        w = self.ui_create_disp_mode_dropdown(frm)
        w.grid(row=6, column=1)
        frm.add_widget(w)

        return frm

    def calc_signal_rms(self):
        return np.power(10, (self.amplitude_dBV / 20))

    def calc_noise_rms(self):
        return np.power(10, (self.noise_dBV / 20))

    def _calc_noise_sigma(self):
        return np.sqrt(2) * self.calc_noise_rms()

    def calc_signal(self, t: np.ndarray) -> np.ndarray:
        phi = np.sqrt(2) * self.calc_signal_rms() * np.exp(1j * 2 * np.pi * (self.freq_mult) * t)
        return np.real(phi) + np.random.normal(0, self._calc_noise_sigma(), len(t))


class Ch03PsdFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh03Psd = default_store().get_config(ConfigCh03Psd)

        self.ctrl_frm = self._create_control()
        self.ctrl_frm.pack(side=LEFT)

        signal_frm = self._create_signal_canvas()
        signal_frm.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigCh03PsdFrame:
        frm: ConfigCh03PsdFrame = self._config.make_config_widget(self)
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
        LENGTH = 512

        self.ctrl_frm.wdg_signal_rms.configure(text=f'{self._config.calc_signal_rms()}')
        self.ctrl_frm.wdg_noise_rms.configure(text=f'{self._config.calc_noise_rms()}')

        np.random.seed(self._config.random_seed)

        self._signal_fig.clear()

        ax_signal = self._signal_fig.add_subplot(2, 1, 1)
        ax_psd = self._signal_fig.add_subplot(2, 1, 2)

        ax_signal.set_xlim(-1.2, 1.2)
        ax_signal.set_xlabel('time')
        ax_signal.set_ylabel('value')
        ax_signal.set_title('Signal')

        #ax_psd.set_xlim(0, 512)
        ax_psd.set_xlabel('frequency')
        ax_psd.set_ylabel('power density')
        ax_psd.set_title('Power Spectral Density')

        # t = np.linspace(-1.0, 1.0, LENGTH)
        t = np.arange(-256, 256, 1) / 256.0
        # f = np.arange(-int(LENGTH/2), int(LENGTH/2), 1)
        f = swap_freq(np.fft.fftfreq(t.shape[-1], 2.0/LENGTH))

        sig = self._config.calc_signal(t)
        ax_signal.plot(t, sig, label='Signal', linestyle='solid', linewidth=1)
        ax_signal.legend()

        #psd = np.abs(np.fft.fft(np.correlate(sig, sig, mode='same')))
        #psd = np.abs(self._swap(np.fft.fft(sig * scipy.signal.windows.hamming(len(sig)))))

        windowed = sig  # * scipy.signal.windows.hamming(len(sig))
        fftransformed = swap_freq(np.fft.fft(windowed)) / len(sig)
        psd = np.abs(fftransformed)
        if self._config.disp_mode == DisplayMode.Log:
            psd = 20 * np.log10(psd)
            ax_psd.set_ylabel('power density (dbV^2)')
        else:
            ax_psd.set_ylabel('power density (V^2)')
        ax_psd.plot(f, psd, label='PSD', linestyle='solid', linewidth=1)
        ax_psd.legend()

        self._signal_canvas.draw()


class Ch03PsdWindow(Window):
    GROUP = Ch03Group
    TITLE = 'Power Spectral Density'
    FRAME = Ch03PsdFrame


if __name__ == '__main__':
    Ch03PsdWindow.main()

