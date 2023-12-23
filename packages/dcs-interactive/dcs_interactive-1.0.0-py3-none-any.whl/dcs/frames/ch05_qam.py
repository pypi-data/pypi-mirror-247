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
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch05Group
from dcs.utils.filter import create_lp_filter_class
from dcs.utils.iq_mixer import create_iq_oscillator_class, IqUpMixer, IqDownMixer, IqRfBandGenerator, IqRxBasebandGenerator
from dcs.utils.qam_modulation import ModulationMethod, QamBasebandModulator, QamBasebandGenerator
from dcs.utils.symbols import MessageBinarySerializer
from typing import  Dict

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pyplot import Circle, Text
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


SAMPLE_RATE = 10000
FFT_SAMPLES_PER_SYM = 64


IqOscillator = create_iq_oscillator_class(sample_rate=SAMPLE_RATE, imbalance_wdg=True)

TxBasebandFilter = create_lp_filter_class(SAMPLE_RATE, 'TX Baseband')
RxBasebandFilter = create_lp_filter_class(SAMPLE_RATE, 'RX Baseband')


class ConfigCh05QamFrame(ConfigControlFrame):
    wdg_msg_update_btn: ttk.Button


@ui_create
class ConfigCh05Qam(ConfigObject):
    _KEY = 'ch05_qam'

    message: str = 'DCS'
    symbol_rate: confloat(ge=-SAMPLE_RATE/4, lt=SAMPLE_RATE/4, multiple_of=(4.0/SAMPLE_RATE)) = 10.0
    modulation: ModulationMethod = ModulationMethod.QPSK
    tx_lp: TxBasebandFilter = TxBasebandFilter()
    tx_osc: IqOscillator = IqOscillator(freq=100.0)
    noise_dBc: confloat(ge=-160.0, le=40.0, multiple_of=0.1) = -60.0
    random_seed: conint(ge=0, lt=10000) = 1000
    rx_osc: IqOscillator = IqOscillator(freq=100.0)
    rx_lp: RxBasebandFilter = RxBasebandFilter()

    def _mod_frame(self, parent: ConfigCh05QamFrame) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Message:').grid(row=0, column=0)
        # NOTE: Recalculating the message is slow. So only update on click on the Update button.
        self.ui_create_message(frm).grid(row=0, column=1)
        parent.wdg_msg_update_btn = ttk.Button(frm, text='Update')
        parent.wdg_msg_update_btn.grid(row=0, column=2)

        ttk.Label(frm, text='Symbol Rate:').grid(row=1, column=0)
        w = self.ui_create_symbol_rate(frm)
        frm.add_widget(w)
        w.grid(row=1, column=1)
        ttk.Label(frm, text='Hz').grid(row=1, column=2)

        ttk.Label(frm, text='Modulation:').grid(row=2, column=0)
        w = self.ui_create_modulation_dropdown(frm)
        frm.add_widget(w)
        w.grid(row=2, column=1)

        ttk.Label(frm, text='TX Baseband Low Pass Cut-Off:').grid(row=3, column=0)
        w = self.tx_lp.ui_create_cutoff(frm)
        frm.add_widget(w)
        w.grid(row=3, column=1)
        ttk.Label(frm, text='Hz').grid(row=3, column=2)

        return frm

    def _noise_frame(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        ttk.Label(frm, text='Signal-Noise Ratio:').grid(row=0, column=0)
        w = self.ui_create_noise_dBc(frm)
        frm.add_widget(w)
        w.grid(row=0, column=1)
        ttk.Label(frm, text='dBc').grid(row=0, column=2)

        ttk.Label(frm, text='Random Seed:').grid(row=1, column=0)
        w = self.ui_create_random_seed(frm)
        frm.add_widget(w)
        w.grid(row=1, column=1)

        return frm

    def _demod_frame(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        frm1 = self.rx_lp.make_config_widget(frm)
        frm1.pack()
        for w in frm1.ctrl_widgets:
            frm.add_widget(w)

        return frm

    def make_config_widget(self, parent: ttk.Widget) -> ConfigCh05QamFrame:
        frm = ConfigCh05QamFrame(parent, borderwidth=1, relief='raised')

        sym_frm = self._mod_frame(frm)
        sym_frm.pack()
        for w in sym_frm.ctrl_widgets:
            frm.add_widget(w)

        tx_frm = ttk.Frame(frm, borderwidth=1, relief='raised')
        tx_frm.pack()
        ttk.Label(tx_frm, text='TX Oscillator:').pack()
        tx_ctrl_frm = self.tx_osc.make_config_widget(tx_frm)
        tx_ctrl_frm.pack()
        for w in tx_ctrl_frm.ctrl_widgets:
            frm.add_widget(w)

        noise_frm = self._noise_frame(frm)
        noise_frm.pack()
        for w in noise_frm.ctrl_widgets:
            frm.add_widget(w)

        rx_frm = ttk.Frame(frm, borderwidth=1, relief='raised')
        rx_frm.pack()
        ttk.Label(rx_frm, text='RX Oscillator:').pack()
        rx_ctrl_frm = self.tx_osc.make_config_widget(rx_frm)
        rx_ctrl_frm.pack()
        for w in rx_ctrl_frm.ctrl_widgets:
            frm.add_widget(w)

        demod_frm = self._demod_frame(frm)
        demod_frm.pack()
        for w in demod_frm.ctrl_widgets:
            frm.add_widget(w)

        return frm


class Ch05QamFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh05Qam = default_store().get_config(ConfigCh05Qam)

        ctrl_frm = self._create_control()
        ctrl_frm.pack(side=LEFT)

        signal_frm = self._create_signal_tabs()
        signal_frm.pack(expand=True, fill=BOTH)

    def _create_control(self) -> ConfigControlFrame:
        frm = self._config.make_config_widget(self)
        frm.widgets_on_change(self._on_change)
        frm.wdg_msg_update_btn.configure(command=lambda: self._on_change(0, 0, 0))
        return frm

    def _on_change(self, _, __, ___):
        default_store().save()
        self.refresh()

    def _create_signal_tabs(self) -> ttk.Widget:
        tabs = ttk.Notebook(self)

        tx_frm = ttk.Frame(tabs)
        tabs.add(tx_frm, text='TX Baseband')
        self._tx_fig = Figure(figsize=(12, 6), dpi=100)
        self._tx_canvas = FigureCanvasTkAgg(self._tx_fig, tx_frm)
        self._tx_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        tx_tb = NavigationToolbar2Tk(self._tx_canvas, tx_frm, pack_toolbar=False)
        tx_tb.pack(side=BOTTOM)

        self._data_bytes = ttk.Label(tx_frm, text='')
        self._data_bytes.pack(side=BOTTOM)
        self._data_syms = ttk.Label(tx_frm, text='')
        self._data_syms.pack(side=BOTTOM)

        hf_frm = ttk.Frame(tabs)
        tabs.add(hf_frm, text='HF Band')
        self._hf_fig = Figure(figsize=(12, 6), dpi=100)
        self._hf_canvas = FigureCanvasTkAgg(self._hf_fig, hf_frm)
        self._hf_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        hf_tb = NavigationToolbar2Tk(self._hf_canvas, hf_frm, pack_toolbar=False)
        hf_tb.pack(side=BOTTOM)

        rx_frm = ttk.Frame(tabs)
        tabs.add(rx_frm, text='RX Baseband')
        self._rx_fig = Figure(figsize=(12, 6), dpi=100)
        self._rx_canvas = FigureCanvasTkAgg(self._rx_fig, rx_frm)
        self._rx_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        rx_tb = NavigationToolbar2Tk(self._rx_canvas, rx_frm, pack_toolbar=False)
        rx_tb.pack(side=BOTTOM)

        self.refresh()

        return tabs

    def refresh(self):
        # Make constellation
        constellation = self._config.modulation.make_constellation_map_str()

        # Make symbols vector
        bytes_symbols = MessageBinarySerializer(self._config.message).to_symbols()
        symbols = bytes_symbols.reencode(self._config.modulation.bits_per_symbol())

        # Update symbol output widgets
        data_bytes = ', '.join(bytes_symbols.to_bit_str())
        self._data_bytes.configure(text=f'Data = [{data_bytes}]')
        data_syms = ', '.join(symbols.to_bit_str())
        self._data_syms.configure(text=f'Symbols = [{data_syms}]')

        # Create signal generators
        baseband_gen = QamBasebandGenerator(
            symbols,
            QamBasebandModulator(
                method=self._config.modulation,
                baseband_filter=self._config.tx_lp,
                symbol_rate=self._config.symbol_rate
            )
        )
        iq_mod = baseband_gen.make_rf_band_generator(
            IqUpMixer(
                tx_osc=self._config.tx_osc,
                noise_dBc=self._config.noise_dBc,
                random_seed=self._config.random_seed
            )
        )
        iq_demod = iq_mod.make_iq_down_mixer(
            IqDownMixer(
                rx_osc=self._config.rx_osc,
                baseband_filter=self._config.rx_lp
            )
        )

        # Draw
        self.draw_tx(constellation, baseband_gen)
        self.draw_hf(iq_mod)
        self.draw_rx(constellation, iq_demod)

    def draw_tx(self, constellation: Dict[str, complex], baseband_gen: QamBasebandGenerator):
        self._tx_fig.clear()

        ax_const = self._tx_fig.add_subplot(2, 1, 1)
        ax_const.set_xlim(-1.2, 1.2)
        ax_const.set_ylim(-1.2, 1.2)
        ax_const.set_xlabel('real')
        ax_const.set_ylabel('imaginary')
        ax_const.set_title('Ideal Constellation Diagram')
        ax_const.set_aspect(1)
        ax_base = self._tx_fig.add_subplot(2, 1, 2)
        ax_base.set_xlabel('time')
        ax_base.set_ylabel('value')
        ax_base.set_title('TX Baseband Signal')

        for sym_str, sym_val in constellation.items():
            circ = Circle((sym_val.real, sym_val.imag), 0.03, alpha=0.4, color='blue', label=sym_str)
            ax_const.add_artist(circ)
            txt = Text(sym_val.real, sym_val.imag, sym_str, color='orange', fontsize=8)
            ax_const.add_artist(txt)

        sig_base_tx = baseband_gen.generate_tx_baseband_signal(SAMPLE_RATE)
        ax_base.set_xlim(np.min(sig_base_tx.t), np.max(sig_base_tx.t))
        ax_base.plot(sig_base_tx.t, np.real(sig_base_tx.signal), label='Baseband I', linestyle='solid', color='blue', linewidth=1)
        ax_base.plot(sig_base_tx.t, np.imag(sig_base_tx.signal), label='Baseband Q', linestyle='solid', color='red', linewidth=1)
        ax_base.legend()

        self._tx_fig.tight_layout()
        self._tx_canvas.draw()

    def draw_hf(self, rf_gen: IqRfBandGenerator):
        self._hf_fig.clear()

        ax_td = self._hf_fig.add_subplot(2, 1, 1)
        ax_td.set_xlabel('time')
        ax_td.set_ylabel('value')
        ax_td.set_title('HF Signal Time-Domain')
        ax_fd = self._hf_fig.add_subplot(2, 1, 2)
        ax_fd.set_ylim(-140, 40)
        ax_fd.set_xlabel('frequency')
        ax_fd.set_ylabel('value (logarithmic)')
        ax_fd.set_title('HF Signal Frequency-Domain')

        sig_hf_normal = rf_gen.generate_rf_signal(SAMPLE_RATE)
        ax_td.set_xlim(np.min(sig_hf_normal.t), np.max(sig_hf_normal.t))
        ax_td.plot(sig_hf_normal.t, np.real(sig_hf_normal.signal), label='HF', linestyle='solid', color='brown', linewidth=1)
        ax_td.legend()

        fd_smp_rate = FFT_SAMPLES_PER_SYM * self._config.symbol_rate
        sig_hf_ovs = rf_gen.generate_rf_signal(fd_smp_rate)
        f_fd, X_hf_fd = sig_hf_ovs.fft(window_fn=scipy.signal.windows.blackman)

        ax_fd.set_xlim(0, np.max(f_fd))
        ax_fd.plot(f_fd, X_hf_fd, label='HF', linestyle='solid', color='brown', linewidth=1)
        ax_fd.legend()

        self._hf_fig.tight_layout()
        self._hf_canvas.draw()

    def draw_rx(self, constellation: Dict[str, complex], rx_gen: IqRxBasebandGenerator):
        self._rx_fig.clear()
        ax_base = self._rx_fig.add_subplot(2, 1, 1)
        ax_base.set_xlabel('time')
        ax_base.set_ylabel('value')
        ax_base.set_title('RX Baseband Signal')
        ax_const = self._rx_fig.add_subplot(2, 1, 2)
        ax_const.set_xlim(-1.2, 1.2)
        ax_const.set_ylim(-1.2, 1.2)
        ax_const.set_xlabel('real')
        ax_const.set_ylabel('imaginary')
        ax_const.set_title('RX Constellation Diagram')
        ax_const.set_aspect(1)

        sig_base_rx = rx_gen.generate_rx_baseband_signal(SAMPLE_RATE)
        ax_base.set_xlim(np.min(sig_base_rx.t), np.max(sig_base_rx.t))
        ax_base.plot(sig_base_rx.t, np.real(sig_base_rx.signal), label='Baseband I', linestyle='solid', color='blue', linewidth=1)
        ax_base.plot(sig_base_rx.t, np.imag(sig_base_rx.signal), label='Baseband Q', linestyle='solid', color='red', linewidth=1)
        ax_base.legend()

        ax_const.plot(np.real(sig_base_rx.signal), np.imag(sig_base_rx.signal), label='Baseband', linestyle='solid', color='purple', linewidth=1)
        ax_const.legend()

        for sym_str, sym_val in constellation.items():
            circ = Circle((sym_val.real, sym_val.imag), 0.05, alpha=0.4, color='blue', label=sym_str)
            ax_const.add_artist(circ)
            txt = Text(sym_val.real, sym_val.imag, sym_str, color='orange', fontsize=8)
            ax_const.add_artist(txt)

        self._rx_fig.tight_layout()
        self._rx_canvas.draw()


class Ch05QamWindow(Window):
    GROUP = Ch05Group
    TITLE = 'Quadrature Amplitude Modulation'
    FRAME = Ch05QamFrame


if __name__ == '__main__':
    Ch05QamWindow.main()

