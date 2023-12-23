#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import copy
from tkinter import ttk, LEFT, BOTH, BOTTOM
from pydantic import confloat, conint
from dcs.config import default_store, ConfigObject, ui_create, ConfigControlFrame
import numpy as np
import scipy.signal
from dcs.frames.base import BaseFrame, Window
from dcs.frames.groups import Ch07Group
from dcs.utils.chain import TxBasebandGenerator, RxCorrelationGenerator, RfBandGenerator
from dcs.utils.filter import create_lp_filter_class, NoFilter
from dcs.utils.iq_mixer import create_iq_oscillator_class, IqUpMixer, IqDownMixer, IqRfBandGenerator, \
    IqRxBasebandGenerator, IqTxBasebandGenerator, IqOscillatorBase
from dcs.utils.qam_modulation import ModulationMethod, QamBasebandModulator, QamBasebandGenerator
from dcs.utils.symbols import MessageBinarySerializer, Symbols
from dcs.utils.spreading import create_spreading_config_class, Spreader, Despreader, SpreadedBasebandSpectrum3D
from typing import Dict, List

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pyplot import Circle, Text
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


SAMPLE_RATE = 10000
FFT_SAMPLES_PER_SYM = 128

TxBasebandFilter = create_lp_filter_class(SAMPLE_RATE, 'TX Baseband')

Spreading = create_spreading_config_class(SAMPLE_RATE)


@ui_create
class User(ConfigObject):
    message: str = 'DCS'
    spreading: Spreading = Spreading()
    modulation: ModulationMethod = ModulationMethod.BPSK
    tx_lp: TxBasebandFilter = TxBasebandFilter()

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent)

        frm1 = ConfigControlFrame(frm, borderwidth=1, relief='raised')
        frm1.pack()
        spreading_frame = self.spreading.make_config_widget(frm1)
        spreading_frame.pack()

        frm2 = ConfigControlFrame(frm, borderwidth=1, relief='raised')
        frm2.pack()
        ttk.Label(frm2, text='Message:').grid(row=0, column=0)
        self.ui_create_message(frm2).grid(row=0, column=1)

        ttk.Label(frm2, text='Modulation:').grid(row=1, column=0)
        self.ui_create_modulation_dropdown(frm2).grid(row=1, column=1)

        ttk.Label(frm2, text='TX Baseband Low Pass Cut-Off:').grid(row=2, column=0)
        self.tx_lp.ui_create_cutoff(frm2).grid(row=2, column=1)
        ttk.Label(frm2, text='Hz').grid(row=2, column=2)

        return frm

    def make_title(self):
        return f'{self.message} - {self.spreading.make_title()}'

    def get_symbols(self) -> Symbols:
        return MessageBinarySerializer(self.message).to_symbols()

    def make_unspreaded_signal(self) -> TxBasebandGenerator:
        return QamBasebandGenerator(
            self.get_symbols(),
            QamBasebandModulator(
                symbol_rate=self.make_spreader().get_symbol_rate(),
                method=ModulationMethod.BPSK,
                baseband_filter=NoFilter(),
            )
        )

    def make_spreader(self) -> Spreader:
        return self.spreading.make_spreader(self.modulation, self.tx_lp)

    def make_despreader(self) -> Despreader:
        return self.spreading.make_despreader(self.modulation, self.tx_lp)


@ui_create
class ConfigCh07Spreading(ConfigObject):
    _KEY = 'ch07_spreading'

    users: List[User] = [
        User()
    ]
    #tx_osc: IqOscillator = IqOscillator(freq=100.0)
    noise_dBc: confloat(ge=-160.0, le=40.0, multiple_of=0.1) = -60.0
    random_seed: conint(ge=0, lt=10000) = 1000
    #rx_osc: IqOscillator = IqOscillator(freq=100.0)
    #rx_lp: RxBasebandFilter = RxBasebandFilter()

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

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ConfigControlFrame(parent, borderwidth=1, relief='raised')

        user_frm = ttk.Frame(frm, borderwidth=1, relief='raised')
        user_frm.pack()
        ttk.Label(user_frm, text='TX Oscillator:').pack()
        w = self.ui_create_users_list(user_frm, lambda e: e.make_title())
        frm.add_widget(w)
        w.pack()

        noise_frm = self._noise_frame(frm)
        noise_frm.pack()
        for w in noise_frm.ctrl_widgets:
            frm.add_widget(w)

        return frm


class Ch07SpreadingFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._config: ConfigCh07Spreading = default_store().get_config(ConfigCh07Spreading)

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

        fd_frm = ttk.Frame(tabs)
        tabs.add(fd_frm, text='Frequency Domain')
        self._fd_fig = Figure(figsize=(12, 6), dpi=100)
        self._fd_canvas = FigureCanvasTkAgg(self._fd_fig, fd_frm)
        self._fd_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        fd_tb = NavigationToolbar2Tk(self._fd_canvas, fd_frm, pack_toolbar=False)
        fd_tb.pack(side=BOTTOM)

        rx_frm = ttk.Frame(tabs)
        tabs.add(rx_frm, text='RX Cross-Correlation')
        self._rx_fig = Figure(figsize=(12, 6), dpi=100)
        self._rx_canvas = FigureCanvasTkAgg(self._rx_fig, rx_frm)
        self._rx_canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        rx_tb = NavigationToolbar2Tk(self._rx_canvas, rx_frm, pack_toolbar=False)
        rx_tb.pack(side=BOTTOM)

        self.refresh()

        return tabs

    def refresh(self):
        if len(self._config.users) > 0:
            user0 = self._config.users[0]
            user0_spreader = user0.make_spreader()
            tx_gen0 = user0_spreader.make_tx_baseband_generator(user0.get_symbols())

            unspreaded_gen0 = user0.make_unspreaded_signal()

            tx_gens = copy.deepcopy(tx_gen0)
            for user in self._config.users[1:]:
                tx_gens += user.make_spreader().make_tx_baseband_generator(user.get_symbols())

            class _Osc(IqOscillatorBase):
                def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
                    pass  # Won't be called

            rf_gen = IqRfBandGenerator(
                tx_gens,
                IqUpMixer(
                    tx_osc=_Osc(freq=0),
                    noise_dBc=self._config.noise_dBc,
                    random_seed=self._config.random_seed,
                )
            )
            # rx_gen = rf_gen.make_iq_down_mixer(
            #     IqDownMixer(
            #         rx_osc=_Osc(freq=0),
            #         baseband_filter=NoFilter(),
            #     )
            # )

            rx_gen = user0.make_despreader().make_rx_correlation_generator(rf_gen)

            # Draw
            self.draw_tx(tx_gen0, unspreaded_gen0, rf_gen)
            self.draw_fd(rf_gen, user0_spreader)
            self.draw_rx(rx_gen, unspreaded_gen0)

    def draw_tx(self, tx_gen0: TxBasebandGenerator, unspreaded_gen0: TxBasebandGenerator, rf_gen: RfBandGenerator):
        self._tx_fig.clear()

        ax_msg = self._tx_fig.add_subplot(3, 1, 1)
        ax_msg.set_xlabel('time')
        ax_msg.set_ylabel('value')
        ax_msg.set_title('User 0 Message (Binary)')
        ax_u0 = self._tx_fig.add_subplot(3, 1, 2)
        ax_u0.set_xlabel('time')
        ax_u0.set_ylabel('value')
        ax_u0.set_title('User 0 TX Baseband Signal')
        ax_tx = self._tx_fig.add_subplot(3, 1, 3)
        ax_tx.set_xlabel('time')
        ax_tx.set_ylabel('value')
        ax_tx.set_title('TX Baseband Signal')

        sig_msg = unspreaded_gen0.generate_tx_baseband_signal(SAMPLE_RATE)
        ax_msg.set_xlim(np.min(sig_msg.t), np.max(sig_msg.t))
        ax_msg.plot(sig_msg.t, np.real(sig_msg.signal), label='Message', color='blue', linewidth=1)

        sig_u0 = tx_gen0.generate_tx_baseband_signal(SAMPLE_RATE)
        ax_u0.set_xlim(np.min(sig_u0.t), np.max(sig_u0.t))
        ax_u0.plot(sig_u0.t, np.real(sig_u0.signal), label='User 0', color='red', linewidth=1)

        sig_tx = rf_gen.generate_rf_signal(SAMPLE_RATE)
        ax_tx.set_xlim(np.min(sig_tx.t), np.max(sig_tx.t))
        ax_tx.plot(sig_tx.t, np.real(sig_tx.signal), label='Baseband', color='brown', linewidth=1)

        self._tx_fig.tight_layout()
        self._tx_canvas.draw()

    def draw_fd(self, rf_gen: RfBandGenerator, spreader: Spreader):
        self._fd_fig.clear()

        ax_fd = self._fd_fig.add_subplot(1, 1, 1, projection='3d')
        ax_fd.set_xlabel('frequency')
        ax_fd.set_ylabel('symbol')
        ax_fd.set_zlabel('value (logarithmic)')
        ax_fd.set_title('HF Signal Frequency-Domain')
        ax_fd.set_zlim(-120, 40)

        x, y, z = SpreadedBasebandSpectrum3D(
            rf_gen,
            spreader.get_symbol_rate(),
            FFT_SAMPLES_PER_SYM
        ).make_plot_data()

        ax_fd.plot_trisurf(x, y, z)

        self._fd_fig.tight_layout()
        self._fd_canvas.draw()

    def draw_rx(self, rx_correlation: RxCorrelationGenerator, unspreaded_gen0: TxBasebandGenerator):
        self._rx_fig.clear()

        ax_msg = self._rx_fig.add_subplot(2, 1, 1)
        ax_msg.set_xlabel('time')
        ax_msg.set_ylabel('value')
        ax_msg.set_title('User 0 Message (Binary)')
        ax_correlation = self._rx_fig.add_subplot(2, 1, 2)
        ax_correlation.set_xlabel('time')
        ax_correlation.set_ylabel('value')
        ax_correlation.set_title('RX Correlation')

        sig_msg = unspreaded_gen0.generate_tx_baseband_signal(SAMPLE_RATE)
        ax_msg.set_xlim(np.min(sig_msg.t), np.max(sig_msg.t))
        ax_msg.plot(sig_msg.t, np.real(sig_msg.signal), label='Message', color='blue', linewidth=1)

        corr = rx_correlation.generate_rx_correlation(SAMPLE_RATE)
        ax_correlation.set_xlim(np.min(corr.t), np.max(corr.t))
        ax_correlation.plot(corr.t, np.real(corr.signal), label='Correlation', color='blue', linewidth=1)

        self._rx_fig.tight_layout()
        self._rx_canvas.draw()


class Ch07SpreadingWindow(Window):
    GROUP = Ch07Group
    TITLE = 'Spread Spectrum'
    FRAME = Ch07SpreadingFrame


if __name__ == '__main__':
    Ch07SpreadingWindow.main()

