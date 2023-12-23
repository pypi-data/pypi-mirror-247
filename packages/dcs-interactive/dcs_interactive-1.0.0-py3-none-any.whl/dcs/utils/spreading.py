#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk
from pydantic import confloat
from dcs.config import ConfigObject, ui_create, ConfigControlFrame
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import numpy as np
from typing import Optional, Type, Callable, Tuple
from .signal import Signal
from .chain import RfBandGenerator, TxBasebandGenerator, RxCorrelationGenerator
from .filter import Filter, NoFilter
from .iq_mixer import IqTxBasebandGenerator
from .qam_modulation import ModulationMethod, QamBasebandModulator, QamBasebandGenerator
from .symbols import Symbols


#####################################################################
# Configuration Items


class SpreadingMethod(str, Enum):
    DSSS_ASYNC = 'Asynchronous CDMA / DSSS'

    def get_spreader(self) -> Type[Spreader]:
        return {
            self.DSSS_ASYNC: AsyncDsssSpreader
        }[self]

    def get_despreader(self) -> Type[Despreader]:
        return {
            self.DSSS_ASYNC: AsyncDsssDespreader
        }[self]


class SpreadingCode(ABC):
    @abstractmethod
    def get_code(self) -> CodeSequence:
        ...

    def get_spreading_factor(self) -> int:
        return self.get_code().sequence.bits_per_symbol

    def get_hopping_length(self) -> int:
        return len(self.get_code().sequence)


class AsyncSpreadingCode(SpreadingCode, ABC):
    pass


class AsyncDsssCode(str, Enum):
    IEEE80211B = 'IEEE 802.11b'

    def make_code(self) -> SpreadingCode:
        code = self

        class _Code(AsyncSpreadingCode):
            def get_code(self) -> CodeSequence:
                return {
                    AsyncDsssCode.IEEE80211B: CodeSequence(
                        sequence=Symbols(
                            # symbols=[1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0b01001000111],
                            symbols=[0b01001000111],
                            bits_per_symbol=11
                        )
                    ),
                }[code]

        return _Code()


@ui_create
class SpreadingConfigBase(ConfigObject, ABC):
    method: SpreadingMethod = SpreadingMethod.DSSS_ASYNC
    async_dsss_code: AsyncDsssCode = AsyncDsssCode.IEEE80211B
    chip_rate: confloat(ge=0) = 10.0

    @abstractmethod
    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        ...

    @abstractmethod
    def _get_chip_rate(self) -> float:
        ...

    def make_title(self):
        if self.method == SpreadingMethod.DSSS_ASYNC:
            return f'DSSS Code: {self.async_dsss_code.value}'
        else:
            raise ValueError(f'Invalid spreading method {self.method}')

    def _get_code(self) -> SpreadingCode:
        if self.method == SpreadingMethod.DSSS_ASYNC:
            return self.async_dsss_code.make_code()
        else:
            raise ValueError(f'Invalid spreading method {self.method}')

    def make_spreader(self, modulation: ModulationMethod, baseband_filter: Filter):
        cls = self.method.get_spreader()
        return cls(
            code=self._get_code(),
            chip_rate=self._get_chip_rate(),
            modulation=modulation,
            baseband_filter=baseband_filter
        )

    def make_despreader(self, modulation: ModulationMethod, baseband_filter: Filter):
        cls = self.method.get_despreader()
        return cls(
            code=self._get_code(),
            chip_rate=self._get_chip_rate(),
            modulation=modulation,
            baseband_filter=baseband_filter
        )


def create_spreading_config_class(sample_rate: int, global_chip_rate: Optional[Callable[[], float]] = None):
    @ui_create
    class _SpreadingConfig(SpreadingConfigBase):
        chip_rate: confloat(ge=0, lt=sample_rate/4, multiple_of=(4.0/sample_rate)) = 10.0

        def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
            frm = ConfigControlFrame(parent)

            ttk.Label(frm, text='Spreading Method:').grid(row=0, column=0)
            w = self.ui_create_method_dropdown(frm)
            frm.add_widget(w)
            w.grid(row=0, column=1)

            ttk.Label(frm, text='DSSS Code:').grid(row=1, column=0)
            w = self.ui_create_async_dsss_code_dropdown(frm)
            frm.add_widget(w)
            w.grid(row=1, column=1)

            # ttk.Label(frm, text='DSSS Code:').grid(row=2, column=0)
            # w = self.ui_create_sync_dsss_code_dropdown(frm)
            # frm.add_widget(w)
            # w.grid(row=2, column=1)

            # ttk.Label(frm, text='FHSS Code:').grid(row=3, column=0)
            # w = self.ui_create_fhss_code_dropdown(frm)
            # frm.add_widget(w)
            # w.grid(row=3, column=1)

            # ttk.Label(frm, text='THSS Code:').grid(row=4, column=0)
            # w = self.ui_create_thss_code_dropdown(frm)
            # frm.add_widget(w)
            # w.grid(row=4, column=1)

            if global_chip_rate is None:
                ttk.Label(frm, text='Chip Rate:').grid(row=5, column=0)
                w = self.ui_create_chip_rate(frm)
                frm.add_widget(w)
                w.grid(row=5, column=1)
                ttk.Label(frm, text='Hz').grid(row=4, column=2)

            return frm

        def _get_chip_rate(self) -> float:
            if global_chip_rate is None:
                return self.chip_rate
            else:
                return global_chip_rate()

    _SpreadingConfig.update_forward_refs(sample_rate=sample_rate)

    return _SpreadingConfig


#####################################################################
# Spectrum Plotting Helper


class SpreadedBasebandSpectrum3D:
    def __init__(self, gen: RfBandGenerator, symbol_rate: float, samples_per_sym: int):
        self.gen = gen
        self.symbol_rate = symbol_rate
        self.samples_per_sym = samples_per_sym

    def make_plot_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        sample_rate = self.symbol_rate * self.samples_per_sym
        base_sig = self.gen.generate_rf_signal(sample_rate)

        symbols_sigs = base_sig.split(self.samples_per_sym)

        x = np.zeros(0)
        y = np.zeros(0)
        z = np.zeros(0)
        for idx, sig in enumerate(symbols_sigs):
            f, fd = sig.fft()
            x = np.concatenate((x, f))
            y = np.concatenate((y, np.ones(len(f)) * idx))
            z = np.concatenate((z, fd))

        return np.real(x), np.real(y), np.real(z)


#####################################################################
# Code


@dataclass
class CodeSequence:
    sequence: Symbols

    def make_qam_bandband_generator(self, chip_rate: float, baseband_filter: Filter) -> QamBasebandGenerator:
        return QamBasebandGenerator(
            self.sequence,
            QamBasebandModulator(
                symbol_rate=chip_rate,
                method=ModulationMethod.BPSK,
                baseband_filter=baseband_filter
            )
        )

    def calc_signal(self, chip_rate: float, sample_rate: float, baseband_filter: Filter = NoFilter()) -> Signal:
        return self.make_qam_bandband_generator(
            chip_rate,
            baseband_filter=baseband_filter
        ).generate_tx_baseband_signal(sample_rate)


#####################################################################
# Spreader


class Spreader(ABC):
    def __init__(self, code: SpreadingCode, chip_rate: float, modulation: ModulationMethod, baseband_filter: Filter):
        self.code = code
        self.chip_rate = chip_rate
        self.modulation = modulation
        self.baseband_filter = baseband_filter

    @abstractmethod
    def make_tx_baseband_generator(self, message: Symbols) -> IqTxBasebandGenerator:
        ...

    def calc_tx_baseband(self, message: Symbols, sample_rate: float) -> Signal:
        gen = self.make_tx_baseband_generator(message)
        return gen.generate_tx_baseband_signal(sample_rate)

    @abstractmethod
    def get_symbol_rate(self) -> float:
        ...


class AsyncDsssSpreader(Spreader):
    def make_tx_baseband_generator(self, message: Symbols) -> IqTxBasebandGenerator:
        assert isinstance(self.code, AsyncSpreadingCode), f'Code must be AsyncSpreadingCode'
        spread_sequence = []
        for msg_sym in message.reencode(1).symbols:
            for code_sym in self.code.get_code().sequence.reencode(1).symbols:
                spread_sequence.append(msg_sym ^ code_sym)
        spread_sym = Symbols(symbols=spread_sequence, bits_per_symbol=1)
        return QamBasebandGenerator(
            symbols=spread_sym,
            qam_mod=QamBasebandModulator(
                method=self.modulation,
                symbol_rate=self.chip_rate,
                baseband_filter=self.baseband_filter
            )
        )

    def get_symbol_rate(self) -> float:
        return self.chip_rate / self.code.get_spreading_factor()


#####################################################################
# Depreader


class CrossCorrelationGenerator(RxCorrelationGenerator):
    def __init__(self, rf_gen: RfBandGenerator, code_signal_gen: TxBasebandGenerator):
        self.rf_gen = rf_gen
        self.code_signal_gen = code_signal_gen

    def generate_rx_correlation(self, sample_rate: float) -> Signal:
        rf = self.rf_gen.generate_rf_signal(sample_rate)
        code = self.code_signal_gen.generate_tx_baseband_signal(sample_rate)
        corr = np.correlate(rf.signal, code.signal, mode='same')
        return Signal(
            t=rf.t,
            signal=corr,
            sample_rate=sample_rate
        )


class Despreader(ABC):
    def __init__(self, code: SpreadingCode, chip_rate: float, modulation: ModulationMethod, baseband_filter: Filter):
        self.code = code
        self.chip_rate = chip_rate
        self.modulation = modulation
        self.baseband_filter = baseband_filter

    @abstractmethod
    def make_rx_correlation_generator(self, rf_gen: RfBandGenerator) -> RxCorrelationGenerator:
        ...

    def calc_rx_correlation(self, rf_gen: RfBandGenerator, sample_rate: float) -> Signal:
        gen = self.make_rx_correlation_generator(rf_gen)
        return gen.generate_rx_correlation(sample_rate)


class AsyncDsssDespreader(Despreader):
    def make_code_signal_generator(self) -> TxBasebandGenerator:
        assert isinstance(self.code, AsyncSpreadingCode), f'Code must be AsyncSpreadingCode'
        return self.code.get_code().make_qam_bandband_generator(self.chip_rate, self.baseband_filter)

    def calc_code_signal(self, sample_rate: float) -> Signal:
        gen = self.make_code_signal_generator()
        return gen.generate_tx_baseband_signal(sample_rate)

    def make_rx_correlation_generator(self, rf_gen: RfBandGenerator) -> RxCorrelationGenerator:
        return CrossCorrelationGenerator(rf_gen, self.make_code_signal_generator())
