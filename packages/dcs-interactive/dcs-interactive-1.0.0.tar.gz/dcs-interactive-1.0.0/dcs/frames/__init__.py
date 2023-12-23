#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List, Type
from . import base

from .ch02_phasor import Ch02PhasorWindow
from .ch02_fourier import Ch02FourierWindow
from .ch03_ergodic import Ch03ErgodicWindow
from .ch03_cross import Ch03CrossCorrelationWindow
from .ch03_psd import Ch03PsdWindow
from .ch04_sampling import Ch04SamplingWindow
from .ch04_window import Ch04WindowWindow
from .ch04_quantization_noise import Ch04QuantizationNoiseWindow
from .ch05_modulation import Ch05ModulationWindow
from .ch05_iq import Ch05IqWindow
from .ch05_qam import Ch05QamWindow
from .ch06_filter import Ch06FilterWindow
from .ch06_mixer import Ch06MixerWindow
from .ch06_down_sampling import Ch06DownSamplingWindow
from .ch06_up_sampling import Ch06UpSamplingWindow
from .ch07_spreading import Ch07SpreadingWindow


def get_windows() -> List[Type[base.Window]]:
    return [
        Ch02PhasorWindow,
        Ch02FourierWindow,
        Ch03ErgodicWindow,
        Ch03CrossCorrelationWindow,
        Ch03PsdWindow,
        Ch04SamplingWindow,
        Ch04WindowWindow,
        Ch04QuantizationNoiseWindow,
        Ch05ModulationWindow,
        Ch05IqWindow,
        Ch05QamWindow,
        Ch06FilterWindow,
        Ch06MixerWindow,
        Ch06DownSamplingWindow,
        Ch06UpSamplingWindow,
        Ch07SpreadingWindow,
    ]


def get_groups() -> List[Type[base.Group]]:
    return base.get_groups(get_windows())


def get_win_of_group(grp: Type[base.Group]) -> List[Type[base.Window]]:
    return base.get_win_of_group(get_windows(), grp)
