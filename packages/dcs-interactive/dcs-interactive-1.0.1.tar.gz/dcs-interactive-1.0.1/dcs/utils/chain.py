#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List
from .signal import Signal


class TxBasebandGenerator(ABC):
    @abstractmethod
    def generate_tx_baseband_signal(self, sample_rate: float) -> Signal:
        ...

    def __add__(self, other: TxBasebandGenerator) -> TxBasebandGenerator:
        class _Combined(TxBasebandGenerator):
            def __init__(self, gen1: TxBasebandGenerator, gen2: TxBasebandGenerator):
                self.ops: List[TxBasebandGenerator] = [gen1, gen2]

            def generate_tx_baseband_signal(self, sample_rate: float) -> Signal:
                summed = self.ops[0].generate_tx_baseband_signal(sample_rate)
                for sig in self.ops[1:]:
                    summed = summed + sig.generate_tx_baseband_signal(sample_rate)
                return summed

            def __add__(self, other: TxBasebandGenerator):
                self.ops.append(other)

        return _Combined(self, other)


class RfBandGenerator(ABC):
    @abstractmethod
    def generate_rf_signal(self, sample_rate: float) -> Signal:
        ...

    def __add__(self, other: RfBandGenerator) -> RfBandGenerator:
        class _Combined(RfBandGenerator):
            def __init__(self, gen1: RfBandGenerator, gen2: RfBandGenerator):
                self.ops: List[RfBandGenerator] = [gen1, gen2]

            def generate_rf_signal(self, sample_rate: float) -> Signal:
                summed = self.ops[0].generate_rf_signal(sample_rate)
                for sig in self.ops[1:]:
                    summed = summed + sig.generate_rf_signal(sample_rate)
                return summed

            def __add__(self, other: RfBandGenerator):
                self.ops.append(other)

        return _Combined(self, other)


class RxBasebandGenerator(ABC):
    @abstractmethod
    def generate_rx_baseband_signal(self, sample_rate: float) -> Signal:
        ...

    def __add__(self, other: RxBasebandGenerator) -> RxBasebandGenerator:
        class _Combined(RxBasebandGenerator):
            def __init__(self, gen1: RxBasebandGenerator, gen2: RxBasebandGenerator):
                self.ops: List[RxBasebandGenerator] = [gen1, gen2]

            def generate_rx_baseband_signal(self, sample_rate: float) -> Signal:
                summed = self.ops[0].generate_rx_baseband_signal(sample_rate)
                for sig in self.ops[1:]:
                    summed = summed + sig.generate_rx_baseband_signal(sample_rate)
                return summed

            def __add__(self, other: RxBasebandGenerator):
                self.ops.append(other)

        return _Combined(self, other)


class RxCorrelationGenerator(ABC):
    @abstractmethod
    def generate_rx_correlation(self, sample_rate: float) -> Signal:
        ...

    def __add__(self, other: RxCorrelationGenerator) -> RxCorrelationGenerator:
        class _Combined(RxCorrelationGenerator):
            def __init__(self, gen1: RxCorrelationGenerator, gen2: RxCorrelationGenerator):
                self.ops: List[RxCorrelationGenerator] = [gen1, gen2]

            def generate_rx_correlation(self, sample_rate: float) -> Signal:
                summed = self.ops[0].generate_rx_correlation(sample_rate)
                for sig in self.ops[1:]:
                    summed = summed + sig.generate_rx_correlation(sample_rate)
                return summed

            def __add__(self, other: RxCorrelationGenerator):
                self.ops.append(other)

        return _Combined(self, other)
