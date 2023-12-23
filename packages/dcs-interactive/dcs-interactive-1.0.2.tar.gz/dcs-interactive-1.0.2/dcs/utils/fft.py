#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import numpy as np


def swap_freq(x: np.ndarray, axis: int = 0) -> np.ndarray:
    transposed = np.swapaxes(x, 0, axis)
    swapped = np.zeros(transposed.shape, dtype=np.complex128)
    length = transposed.shape[0]
    swapped[int(length/2):, ] = transposed[:int(length/2), ]
    swapped[:int(length/2), ] = transposed[int(length/2):, ]
    return np.swapaxes(swapped, axis, 0)


def abs_log_fft(x: np.ndarray, factor: float = 20, axis: int = 0) -> np.ndarray:
    return factor * np.log10(np.abs(swap_freq(np.fft.fft(x), axis)) / len(x))
