#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk, Listbox, LEFT, BOTH, BOTTOM, ACTIVE
from tkinter.simpledialog import Dialog
from pydantic import confloat, conint
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
import scipy.signal
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch06Group
from typing import List, Tuple, Optional
from enum import Enum

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pyplot import Circle
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class FilterType(str, Enum):
    LOW = 'Low-pass'
    HIGH = 'High-pass'
    PASS = 'Band-pass'
    STOP = 'Band-stop'


class FilterDesignMethod(str, Enum):
    BUTTER = 'Butterworth (IIR)'
    CHEBY1 = 'Chebyshev type I (IIR)'
    FIR_WIN = 'Windowing Method (FIR)'


@ui_create
class FilterDesigner(ConfigObject):
    sample_rate: float

    filter_type: FilterType = FilterType.LOW
    cutoff: confloat(ge=0.0, lt=1000.0, multiple_of=0.1) = 25
    width: confloat(ge=0.0, lt=1000.0, multiple_of=0.1) = 5
    design_method: FilterDesignMethod = FilterDesignMethod.BUTTER
    order: conint(ge=0, lt=100) = 7

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent)

        ttk.Label(frm, text='Filter Type:').grid(row=0, column=0)
        w = self.ui_create_filter_type_dropdown(frm)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        ttk.Label(frm, text='Cut-off Frequency:').grid(row=1, column=0)
        w = self.ui_create_cutoff(frm)
        frm.add_widget(w)
        w.grid(row=1, column=1)
        ttk.Label(frm, text='Hz').grid(row=1, column=2)

        ttk.Label(frm, text='Bandwidth (only Band-pass/-stop):').grid(row=2, column=0)
        w = self.ui_create_width(frm)
        frm.add_widget(w)
        w.grid(row=2, column=1)
        ttk.Label(frm, text='Hz').grid(row=2, column=2)

        ttk.Label(frm, text='Design Method:').grid(row=3, column=0)
        w = self.ui_create_design_method_dropdown(frm)
        frm.add_widget(w)
        w.grid(row=3, column=1)

        ttk.Label(frm, text='Filter Order:').grid(row=4, column=0)
        w = self.ui_create_order(frm)
        frm.add_widget(w)
        w.grid(row=4, column=1)

        return frm

    @classmethod
    def make_dialog(cls, parent: ttk.Widget, sample_rate: float) -> Optional[FilterDesigner]:
        class DesignDialog(Dialog):
            def __init__(self, *args, **kwargs):
                self._cfg: FilterDesigner = cls(sample_rate=sample_rate)
                self.config: Optional[FilterDesigner] = None
                super().__init__(*args, **kwargs)

            def body(self, master) -> None:
                frm = self._cfg.make_config_widget(master)
                frm.pack()

            def buttonbox(self):
                box = ttk.Frame(self)

                w = ttk.Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
                w.pack(side=LEFT, padx=5, pady=5)
                self.bind("<Return>", self.ok)

                w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
                w.pack(side=LEFT, padx=5, pady=5)
                self.bind("<Escape>", self.cancel)

                box.pack()

            def apply(self):
                self.config = self._cfg

        diag = DesignDialog(parent)
        return diag.config

    def make_filter(self) -> Tuple[np.ndarray, np.ndarray]:
        iir_param = {
            'N': self.order,
            'Wn': None,
            'btype': '',
            'analog': False,
            'output': 'ba',
            'fs': self.sample_rate,
        }
        fir_param = {
            'numtaps': self.order,
            'cutoff': None,
            'window': 'blackman',
            'pass_zero': '',
            'fs': self.sample_rate,
        }
        if self.filter_type == FilterType.LOW:
            iir_param['Wn'] = self.cutoff
            iir_param['btype'] = 'lowpass'
            fir_param['cutoff'] = self.cutoff
            fir_param['pass_zero'] = 'lowpass'
        elif self.filter_type == FilterType.HIGH:
            iir_param['Wn'] = self.cutoff
            iir_param['btype'] = 'highpass'
            fir_param['cutoff'] = self.cutoff
            fir_param['pass_zero'] = 'highpass'
        elif self.filter_type == FilterType.PASS:
            iir_param['Wn'] = (self.cutoff - (self.width/2), self.cutoff + (self.width/2))
            iir_param['btype'] = 'bandpass'
            fir_param['cutoff'] = (self.cutoff - (self.width/2), self.cutoff + (self.width/2))
            fir_param['pass_zero'] = 'bandpass'
        elif self.filter_type == FilterType.STOP:
            iir_param['Wn'] = (self.cutoff - (self.width/2), self.cutoff + (self.width/2))
            iir_param['btype'] = 'bandstop'
            fir_param['cutoff'] = (self.cutoff - (self.width/2), self.cutoff + (self.width/2))
            fir_param['pass_zero'] = 'bandstop'
        else:
            raise Exception('Invalid filter type')

        if self.design_method == FilterDesignMethod.BUTTER:
            b, a = scipy.signal.butter(**iir_param)
            return b, a
        elif self.design_method == FilterDesignMethod.CHEBY1:
            b, a = scipy.signal.cheby1(**iir_param, rp=1)
            return b, a
        elif self.design_method == FilterDesignMethod.FIR_WIN:
            b = scipy.signal.firwin(**fir_param)
            return b, np.array([])
        else:
            raise Exception('Invalid design method')


@ui_create
class PolyCoeff(ConfigObject):
    real: str = '0.0'
    imag: str = ''

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent)

        ttk.Label(frm, text='Real:').grid(row=0, column=0)
        w = self.ui_create_real(frm)
        frm.add_widget(w)
        w.grid(row=0, column=1)

        ttk.Label(frm, text='Imaginary:').grid(row=1, column=0)
        w = self.ui_create_imag(frm)
        frm.add_widget(w)
        w.grid(row=1, column=1)

        return frm

    def get(self) -> complex:
        val = 0 + 0j
        try:
            val += float(self.real)
            val += 1j * float(self.imag)
        except ValueError:
            pass
        return val

    def make_title(self):
        if self.get().imag == 0:
            return f'{self.get().real}'
        else:
            return f'{self.get().real} + j {self.get().imag}'


class ConfigCh06FilterFrame(ConfigControlFrame):
    wdg_poly_b_box: Listbox
    wdg_poly_a_box: Listbox


@ui_create
class ConfigCh06Filter(ConfigObject):
    _KEY = 'ch06_filter'

    sample_rate: confloat(ge=0.0, lt=1000.0, multiple_of=0.1) = 100
    poly_b: List[PolyCoeff] = [PolyCoeff(real='1.0')]
    poly_a: List[PolyCoeff] = []

    def _sample_cfg(self, parent: ConfigControlFrame):
        frm = ttk.Frame(parent, borderwidth=1, relief='raised')
        frm.pack()

        ttk.Label(frm, text='Sampling Rate:').grid(row=0, column=0)
        w = self.ui_create_sample_rate(frm)
        parent.add_widget(w)
        w.grid(row=0, column=1)
        ttk.Label(frm, text='Hz').grid(row=0, column=2)

    def make_config_widget(self, parent: ttk.Widget) -> ConfigCh06FilterFrame:
        frm = ConfigCh06FilterFrame(parent, borderwidth=1, relief='raised')

        self._sample_cfg(frm)

        ttk.Label(frm, text='Numerator Coefficients:').pack()
        frm.wdg_poly_b_box = self.ui_create_poly_b_list(frm, lambda e: e.make_title())
        frm.add_widget(frm.wdg_poly_b_box)
        frm.wdg_poly_b_box.pack()

        ttk.Label(frm, text='Denominator Coefficients:').pack()
        frm.wdg_poly_a_box = self.ui_create_poly_a_list(frm, lambda e: e.make_title())
        frm.add_widget(frm.wdg_poly_a_box)
        frm.wdg_poly_a_box.pack()

        ttk.Button(frm, text='Generate Filter', command=lambda: self._generate(parent, frm)).pack()

        return frm

    def _generate(self, parent: ttk.Widget, frm: ConfigCh06FilterFrame):
        cfg = FilterDesigner.make_dialog(parent, self.sample_rate)
        if cfg is not None:
            b, a = cfg.make_filter()
            self.poly_b = [PolyCoeff(real=str(x.real), imag=str(x.imag)) for x in b]
            self.poly_a = [PolyCoeff(real=str(x.real), imag=str(x.imag)) for x in a]
            frm.wdg_poly_b_box.sync_in()
            frm.wdg_poly_a_box.sync_in()
            frm.wdg_poly_b_box.sync_out()
            frm.wdg_poly_a_box.sync_out()

    def get_poly(self) -> Tuple[List[complex], List[complex]]:
        b = [x.get() for x in self.poly_b]
        a = [x.get() for x in self.poly_a]
        if len(b) == 0:
            b = [1]
        if len(a) == 0:
            a = [1]
        return b, a

    def get_dlti(self) -> scipy.signal.dlti:
        b, a = self.get_poly()
        return scipy.signal.dlti(b, a, dt=1/self.sample_rate)

    def get_zpk(self) -> Tuple[np.ndarray, np.ndarray, float]:
        b, a = self.get_poly()
        return scipy.signal.tf2zpk(b, a)


class Ch06FilterFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh06Filter = default_store().get_config(ConfigCh06Filter)

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
        self.draw_bode()
        self.draw_impulse()
        self.draw_pz()

    def _create_signal_tabs(self) -> ttk.Widget:
        tabs = ttk.Notebook(self)

        bode_frm = ttk.Frame(tabs)
        tabs.add(bode_frm, text='Bode Plot')
        self._bode_fig = Figure(figsize=(12, 6), dpi=100)
        self._bode_canvas = FigureCanvasTkAgg(self._bode_fig, bode_frm)
        self._bode_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        bode_tb = NavigationToolbar2Tk(self._bode_canvas, bode_frm, pack_toolbar=False)
        bode_tb.pack(side=BOTTOM)

        impulse_frm = ttk.Frame(tabs)
        tabs.add(impulse_frm, text='Impulse Response')
        self._impulse_fig = Figure(figsize=(12, 6), dpi=100)
        self._impulse_canvas = FigureCanvasTkAgg(self._impulse_fig, impulse_frm)
        self._impulse_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        impulse_tb = NavigationToolbar2Tk(self._impulse_canvas, impulse_frm, pack_toolbar=False)
        impulse_tb.pack(side=BOTTOM)

        pz_frm = ttk.Frame(tabs)
        tabs.add(pz_frm, text='Pole-Zero Map')
        self._pz_fig = Figure(figsize=(12, 6), dpi=100)
        self._pz_canvas = FigureCanvasTkAgg(self._pz_fig, pz_frm)
        self._pz_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        pz_tb = NavigationToolbar2Tk(self._pz_canvas, pz_frm, pack_toolbar=False)
        pz_tb.pack(side=BOTTOM)

        self.draw_bode()
        self.draw_impulse()
        self.draw_pz()

        return tabs

    def draw_bode(self):
        self._bode_fig.clear()

        ax_mag = self._bode_fig.add_subplot(2, 1, 1)
        ax_mag.set_xlabel('frequency')
        ax_mag.set_ylabel('magnitude (dB)')
        ax_mag.set_title('Magnitude Plot')
        ax_pha = self._bode_fig.add_subplot(2, 1, 2)
        ax_pha.set_xlabel('frequency')
        ax_pha.set_ylabel('phase (°)')
        ax_pha.set_title('Phase Plot')

        w, mag, pha = scipy.signal.dbode(self._config.get_dlti(), n=1024)
        f = w / (2 * np.pi)
        ax_mag.plot(f, mag, label='Magnitude', linestyle='solid', color='blue', linewidth=1)
        ax_mag.plot((0, np.max(f)), np.array([np.max(mag)-3]).repeat(2), label='-3 dB', linestyle='dotted', color='red', linewidth=1)
        ax_mag.legend()
        ax_pha.plot(f, np.unwrap(pha, discont=360), linestyle='solid', color='green', linewidth=1)

        ax_mag.set_ylim(np.clip(np.min(mag), -80, None), np.max(mag)+5)

        self._bode_fig.tight_layout()
        self._bode_canvas.draw()

    def draw_impulse(self):
        self._impulse_fig.clear()

        ax_ir = self._impulse_fig.add_subplot(1, 1, 1)
        ax_ir.set_xlabel('time')
        ax_ir.set_ylabel('value')
        ax_ir.set_title('Impulse Response')

        try:
            order = len(self._config.poly_b) + len(self._config.poly_a)
            t, y = scipy.signal.dimpulse(self._config.get_dlti(), n=order * 32)
            y = y[0]
            ax_ir.plot(t, np.squeeze(np.real(y)), label='Real', linestyle='solid', color='blue', linewidth=1)
            if (np.min(np.imag(y)) != 0.0) or (np.max(np.imag(y)) != 0.0):
                ax_ir.plot(t, np.squeeze(np.imag(y)), label='Imag', linestyle='solid', color='blue', linewidth=1)
            ax_ir.legend()
        except ValueError as e:
            print(repr(e))

        self._impulse_fig.tight_layout()
        self._impulse_canvas.draw()

    def draw_pz(self):
        self._pz_fig.clear()

        ax_pz = self._pz_fig.add_subplot(1, 1, 1)
        ax_pz.set_xlabel('real')
        ax_pz.set_ylabel('imag')
        ax_pz.set_title('Pole-Zero Map')
        ax_pz.set_aspect(1)

        ax_pz.add_artist(Circle((0, 0), 1, color='red', fill=False, label='Circle of Unity'))

        z, p, k = self._config.get_zpk()
        ax_pz.scatter(np.real(p), np.imag(p), marker='x', label='Poles', color='blue', linewidth=1)
        ax_pz.scatter(np.real(z), np.imag(z), marker='o', label='Zeroes', color='blue', linewidth=1)
        ax_pz.legend()

        concat = np.concatenate((p, z))
        ax_pz.set_xlim(np.clip(np.min(np.real(concat)) + 0.2, None, -1.2), np.clip(np.max(np.real(concat)) + 0.2, 1.2, None))
        ax_pz.set_ylim(np.clip(np.min(np.imag(concat)) + 0.2, None, -1.2), np.clip(np.max(np.imag(concat)) + 0.2, 1.2, None))

        self._pz_fig.tight_layout()
        self._pz_canvas.draw()


class Ch06FilterWindow(Window):
    GROUP = Ch06Group
    TITLE = 'Digital Filter'
    FRAME = Ch06FilterFrame


if __name__ == '__main__':
    Ch06FilterWindow.main()

