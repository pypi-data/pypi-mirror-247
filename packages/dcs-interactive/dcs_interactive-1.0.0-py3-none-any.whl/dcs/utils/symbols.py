#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Symbols:
    symbols: List[int]
    bits_per_symbol: int

    def reencode(self, new_bits_per_symbol: int) -> Symbols:
        assert new_bits_per_symbol > 0, 'Number of bits must be at least 1'
        mask = (1 << new_bits_per_symbol) - 1
        tmp_word = 0
        head = 0
        new_symbols = []
        for sym in self.symbols:
            tmp_word |= (sym << head)
            head += self.bits_per_symbol
            while head >= new_bits_per_symbol:
                new_symbols.append(tmp_word & mask)
                tmp_word >>= new_bits_per_symbol
                head -= new_bits_per_symbol
        if head > 0:
            new_symbols.append(tmp_word & mask)

        return Symbols(
            symbols=new_symbols,
            bits_per_symbol=new_bits_per_symbol,
        )

    def to_bit_str(self) -> List[str]:
        fmt = '{:0%db}' % self.bits_per_symbol
        return [fmt.format(sym) for sym in self.symbols]

    def __len__(self):
        return len(self.symbols)


class MessageBinarySerializer:
    def __init__(self, message: str):
        self.message = message
        self.symbols = None

    def to_symbols(self) -> Symbols:
        if self.symbols is None:
            ba = bytearray(self.message, 'utf-8')
            self.symbols = Symbols(
                symbols=[int(sym) for sym in ba],
                bits_per_symbol=8,
            )
        return self.symbols
