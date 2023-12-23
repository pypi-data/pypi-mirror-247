#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import List, Tuple, Callable
import numpy as np
import scipy.signal
import copy
from dataclasses import dataclass

from .fft import abs_log_fft, swap_freq


@dataclass(init=False)
class Signal:
    t: np.ndarray
    signal: np.ndarray
    sample_rate: float

    def __init__(self, t: np.ndarray, signal: np.ndarray, sample_rate: float):
        assert len(t) == len(signal), 't must have the same length like signal'
        assert np.var(np.max(t[1:] - t[:len(t)-1])) < 1e-9, 't must be equidistant'
        assert (((np.max(t) - np.min(t)) / (len(t) - 1)) - sample_rate) < 1e-9, 't must be spaced with sample period'
        self.t = t
        self.signal = signal
        self.sample_rate = sample_rate

    def fft(self, window_fn: Callable[[int], np.ndarray] = scipy.signal.windows.boxcar) -> Tuple[np.ndarray, np.ndarray]:
        f = swap_freq(np.fft.fftfreq(self.t.shape[-1], 1.0/self.sample_rate))
        x = abs_log_fft(self.signal * window_fn(len(self.signal)))
        return f, x

    def split(self, equiv_length: int) -> List[Signal]:
        parts = []
        t = copy.deepcopy(self.t)
        signal = copy.deepcopy(self.signal)
        while len(t) > equiv_length:
            parts.append(
                Signal(
                    t=t[:equiv_length],
                    signal=signal[:equiv_length],
                    sample_rate=self.sample_rate
                )
            )
            t = t[equiv_length:]
            signal = signal[equiv_length:]
        if len(t) > 0:
            parts.append(
                Signal(
                    t=t[:equiv_length],
                    signal=signal[:equiv_length],
                    sample_rate=self.sample_rate
                )
            )
        return parts

    def __add__(self, other: Signal) -> Signal:
        assert self.t == other.t, 'Time vectors must be the same'
        assert self.sample_rate == other.sample_rate, 'Sampling rate must be equal'
        return Signal(
            t=copy.deepcopy(self.t),
            signal=self.signal + other.signal,
            sample_rate=self.sample_rate
        )
