#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from tkinter import ttk
from pydantic import confloat
from dcs.config import ConfigObject, ui_create, ConfigControlFrame
import scipy.signal
import copy
from abc import abstractmethod, ABC
from typing import Optional

from .signal import Signal


class Filter(ABC):
    @abstractmethod
    def filter(self, signal_in: Signal) -> Signal:
        ...


class NoFilter(Filter):
    def filter(self, signal_in: Signal) -> Signal:
        return copy.deepcopy(signal_in)


class IirFilter(Filter):
    def __init__(self, b, a):
        self.b = b
        self.a = a

    def filter(self, signal_in: Signal) -> Signal:
        zi = scipy.signal.lfilter_zi(self.b, self.a)
        z, _ = scipy.signal.lfilter(self.b, self.a, signal_in.signal, zi=zi*signal_in.signal[0])
        return Signal(
            t=signal_in.t,
            signal=z,
            sample_rate=signal_in.sample_rate,
        )


@ui_create
class LowPassFilterBase(Filter, ConfigObject, ABC):
    cutoff: confloat(ge=0) = 0.0
    n: int = 5
    _off_if_zero: bool = True

    def filter(self, signal_in: Signal) -> Signal:
        if (self.cutoff == 0) and self._off_if_zero:
            return copy.deepcopy(signal_in)
        else:
            # b, a = scipy.signal.butter(N=n, Wn=cutoff, btype='low', fs=self.sample_rate, output='ba')
            b, a = scipy.signal.cheby1(N=self.n, rp=1, Wn=self.cutoff, btype='low', fs=signal_in.sample_rate, output='ba')
            iir = IirFilter(b, a)
            return iir.filter(signal_in)


def create_lp_filter_class(sample_rate: int, title: str, off_if_zero: bool = True, unit: Optional[str] = 'Hz'):
    @ui_create
    class _LowPassFilter(LowPassFilterBase):
        cutoff: confloat(ge=0, lt=sample_rate/4, multiple_of=(4.0/sample_rate)) = 0.0
        _off_if_zero: bool = off_if_zero

        def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
            frm = ConfigControlFrame(parent)

            ttk.Label(frm, text=f'{title} Low Pass Cut-Off:').grid(row=0, column=0)
            w = self.ui_create_cutoff(frm)
            frm.add_widget(w)
            w.grid(row=0, column=1)
            if unit is not None:
                ttk.Label(frm, text=unit).grid(row=0, column=2)

            return frm

    _LowPassFilter.update_forward_refs(sample_rate=sample_rate, off_if_zero=off_if_zero)
    return _LowPassFilter

