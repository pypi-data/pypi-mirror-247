#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk
from pydantic import confloat
from dcs.config import ConfigObject, ui_create, ConfigControlFrame
from typing import Dict
import numpy as np
from abc import abstractmethod, ABC

from .signal import Signal
from .chain import TxBasebandGenerator, RfBandGenerator, RxBasebandGenerator
from .filter import Filter


@ui_create
class IqOscillatorBase(ConfigObject, ABC):
    freq: confloat(ge=0) = 100.0
    phase: confloat(ge=-180.0, le=180.0, multiple_of=0.1) = 0.0
    phase_imbalance: confloat(ge=-90.0, le=90.0, multiple_of=0.01) = 0.0
    amplitude_imbalance: confloat(ge=-1.0, le=1.0, multiple_of=0.001) = 0.0

    def calc_signal(self, t: np.ndarray) -> np.ndarray:
        phase_rad = self.phase * np.pi / 180
        phi = 2 * np.pi * self.freq * t
        out_i = np.cos(phi + phase_rad)
        out_q = (1 + self.amplitude_imbalance) * np.sin(phi + phase_rad + self.phase_imbalance)
        return out_i + (1j * out_q)

    @abstractmethod
    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        ...

    def make_title(self):
        return f'f={self.freq}, phi={self.phase}°'


def create_iq_oscillator_class(sample_rate: int, imbalance_wdg: bool = True):
    @ui_create
    class _IqOscillator(IqOscillatorBase):
        freq: confloat(ge=0, lt=sample_rate/4, multiple_of=(4.0/sample_rate)) = 100.0

        def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
            frm = ConfigControlFrame(parent)

            ttk.Label(frm, text='Frequency:').grid(row=0, column=0)
            w = self.ui_create_freq(frm)
            frm.add_widget(w)
            w.grid(row=0, column=1)

            ttk.Label(frm, text='Phase:').grid(row=1, column=0)
            w = self.ui_create_phase(frm)
            frm.add_widget(w)
            w.grid(row=1, column=1)
            ttk.Label(frm, text='°').grid(row=1, column=2)

            if imbalance_wdg:
                ttk.Label(frm, text='Phase Imbalance:').grid(row=2, column=0)
                w = self.ui_create_phase_imbalance(frm)
                frm.add_widget(w)
                w.grid(row=2, column=1)
                ttk.Label(frm, text='°').grid(row=2, column=2)

                ttk.Label(frm, text='Amplitude Imbalance:').grid(row=3, column=0)
                w = self.ui_create_amplitude_imbalance(frm)
                frm.add_widget(w)
                w.grid(row=3, column=1)
                ttk.Label(frm, text='Rel. Error').grid(row=3, column=2)

            return frm

    _IqOscillator.update_forward_refs(sample_rate=sample_rate)
    return _IqOscillator


class IqUpMixer:
    def __init__(self, tx_osc: IqOscillatorBase, noise_dBc: float, random_seed: int):
        self.tx_osc = tx_osc
        self.noise_dBc = noise_dBc
        self.random_seed = random_seed

    def _make_noise(self, t: np.ndarray) -> np.ndarray:
        np.random.seed(self.random_seed)
        noise_rms = np.power(10, (self.noise_dBc / 20))
        noise_sigma = np.sqrt(2) * noise_rms
        return np.random.normal(0, noise_sigma, len(t))

    def calc_rf_signal(self, tx_baseband_signal: Signal) -> Signal:
        t = tx_baseband_signal.t
        baseband = tx_baseband_signal.signal
        osc = self.tx_osc.calc_signal(t)
        i_mixed = np.real(baseband) * np.real(osc)
        q_mixed = np.imag(baseband) * np.imag(osc)
        return Signal(
            t=t,
            signal=i_mixed - q_mixed + self._make_noise(t),
            sample_rate=tx_baseband_signal.sample_rate,
        )


class IqDownMixer:
    def __init__(self, rx_osc: IqOscillatorBase, baseband_filter: Filter):
        self.rx_osc = rx_osc
        self.baseband_filter = baseband_filter

    def calc_rx_baseband_signal(self, rf_signal: Signal) -> Signal:
        osc = self.rx_osc.calc_signal(rf_signal.t)
        i_mixed = 2 * rf_signal.signal * np.real(osc)
        q_mixed = 2 * rf_signal.signal * np.imag(osc)
        base = i_mixed - (1j * q_mixed)
        return self.baseband_filter.filter(
            Signal(
                t=rf_signal.t,
                signal=base,
                sample_rate=rf_signal.sample_rate,
            )
        )


class IqTxBasebandGenerator(TxBasebandGenerator, ABC):
    @abstractmethod
    def generate_tx_baseband_signal(self, sample_rate: float) -> Signal:
        ...

    def make_rf_band_generator(self, up_mix: IqUpMixer) -> IqRfBandGenerator:
        return IqRfBandGenerator(self, up_mix)


class IqRfBandGenerator(RfBandGenerator):
    def __init__(self, tx_baseband_generator: IqTxBasebandGenerator, up_mix: IqUpMixer):
        self.tx_baseband_generator = tx_baseband_generator
        self.up_mix = up_mix
        self._lazy_eval_store: Dict[float, Signal] = {}

    def generate_rf_signal(self, sample_rate: float) -> Signal:
        if sample_rate not in self._lazy_eval_store:
            tx_baseband_signal = self.tx_baseband_generator.generate_tx_baseband_signal(sample_rate)
            self._lazy_eval_store[sample_rate] = self.up_mix.calc_rf_signal(tx_baseband_signal)
        return self._lazy_eval_store[sample_rate]

    def make_iq_down_mixer(self, down_mix: IqDownMixer) -> IqRxBasebandGenerator:
        return IqRxBasebandGenerator(self, down_mix)


class IqRxBasebandGenerator(RxBasebandGenerator):
    def __init__(self, rf_generator: IqRfBandGenerator, down_mix: IqDownMixer):
        self.rf_generator = rf_generator
        self.down_mix = down_mix
        self._lazy_eval_store: Dict[float, Signal] = {}

    def generate_rx_baseband_signal(self, sample_rate: float) -> Signal:
        if sample_rate not in self._lazy_eval_store:
            rf_signal = self.rf_generator.generate_rf_signal(sample_rate)
            self._lazy_eval_store[sample_rate] = self.down_mix.calc_rx_baseband_signal(rf_signal)
        return self._lazy_eval_store[sample_rate]
