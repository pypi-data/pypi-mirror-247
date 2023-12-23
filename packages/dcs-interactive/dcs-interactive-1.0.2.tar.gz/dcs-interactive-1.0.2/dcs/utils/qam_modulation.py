#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Dict
from enum import Enum
import numpy as np

from .signal import Signal
from .filter import Filter
from .iq_mixer import IqTxBasebandGenerator
from .symbols import Symbols


class ModulationMethod(str, Enum):
    ASK = 'ASK'
    BPSK = 'BPSK'
    QPSK = 'QPSK'
    PSK8 = '8-PSK'
    QAM16 = '16-QAM'
    QAM64 = '64-QAM'
    QAM256 = '256-QAM'

    @classmethod
    def _make_constellation_psk(cls, points: int) -> List[complex]:
        prim_root = np.exp(1j * 2 * np.pi / points)
        return np.power(prim_root, np.arange(0, points))

    @classmethod
    def _make_constellation_qam(cls, points: int) -> List[complex]:
        dim = int(np.sqrt(points))
        const = []
        for x in np.linspace(-1.0, 1.0, dim):
            for y in np.linspace(-1.0, 1.0, dim):
                sym = x + (1j * y)
                const.append(sym)
        return const

    def make_constellation(self) -> List[complex]:
        if self == ModulationMethod.ASK:
            return [0.2, 1.0]
        elif self == ModulationMethod.BPSK:
            return self._make_constellation_psk(2)
        elif self == ModulationMethod.QPSK:
            return self._make_constellation_psk(4)
        elif self == ModulationMethod.PSK8:
            return self._make_constellation_psk(8)
        elif self == ModulationMethod.QAM16:
            return self._make_constellation_qam(16)
        elif self == ModulationMethod.QAM64:
            return self._make_constellation_qam(64)
        elif self == ModulationMethod.QAM256:
            return self._make_constellation_qam(256)
        else:
            raise Exception('Unknown modulation')

    def bits_per_symbol(self) -> int:
        if self == ModulationMethod.ASK:
            return 1
        elif self == ModulationMethod.BPSK:
            return 1
        elif self == ModulationMethod.QPSK:
            return 2
        elif self == ModulationMethod.PSK8:
            return 3
        elif self == ModulationMethod.QAM16:
            return 4
        elif self == ModulationMethod.QAM64:
            return 6
        elif self == ModulationMethod.QAM256:
            return 8
        else:
            raise Exception('Unknown modulation')

    def make_constellation_str(self) -> List[str]:
        return [f'{idx:0{self.bits_per_symbol()}b}' for idx in range(2**self.bits_per_symbol())]

    def make_constellation_map(self) -> Dict[int, complex]:
        constell = self.make_constellation()
        return {idx: constell[idx] for idx in range(2 ** self.bits_per_symbol())}

    def make_constellation_map_str(self) -> Dict[str, complex]:
        constell = self.make_constellation()
        str_list = self.make_constellation_str()
        return {str_list[idx]: constell[idx] for idx in range(2 ** self.bits_per_symbol())}


class QamBasebandModulator:
    def __init__(self, symbol_rate: float, method: ModulationMethod, baseband_filter: Filter):
        self.symbol_rate = symbol_rate
        self.method = method
        self.baseband_filter = baseband_filter

    def _to_iq_symbols(self, symbols: Symbols) -> List[complex]:
        lut = self.method.make_constellation()
        return [lut[x] for x in symbols.symbols]

    def _make_t_vec(self, symbols: Symbols, sample_rate: float) -> np.ndarray:
        t_end = len(symbols) * (1 / self.symbol_rate)
        n_smpls = int(t_end * sample_rate)
        return np.arange(0, n_smpls, 1) / sample_rate

    def calc_tx_baseband_signal(self, symbols: Symbols, sample_rate: float) -> Signal:
        reenc_syms = symbols.reencode(self.method.bits_per_symbol())
        syms = self._to_iq_symbols(reenc_syms)
        t = self._make_t_vec(reenc_syms, sample_rate)
        idx_vec = [int(x) for x in np.floor(t * self.symbol_rate)]
        return self.baseband_filter.filter(
            Signal(
                t=t,
                signal=np.array([syms[idx] if 0 <= idx < len(syms) else 0 for idx in idx_vec]),
                sample_rate=sample_rate,
            )
        )


class QamBasebandGenerator(IqTxBasebandGenerator):
    def __init__(self, symbols: Symbols, qam_mod: QamBasebandModulator):
        self.symbols = symbols
        self.qam_mod = qam_mod
        self._lazy_eval_store: Dict[float, Signal] = {}

    def generate_tx_baseband_signal(self, sample_rate: float) -> Signal:
        if sample_rate not in self._lazy_eval_store:
            self._lazy_eval_store[sample_rate] = self.qam_mod.calc_tx_baseband_signal(self.symbols, sample_rate)
        return self._lazy_eval_store[sample_rate]
