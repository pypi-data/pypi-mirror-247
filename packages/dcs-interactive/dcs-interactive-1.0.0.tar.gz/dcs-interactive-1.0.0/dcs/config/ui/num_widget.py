#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from typing import Type
from tkinter import ttk, StringVar
from pydantic import ConstrainedInt, ConstrainedFloat

from .base import make_config_widget_base


class NumWidget(make_config_widget_base(ttk.Spinbox)):
    MODEL_TYPE = int | float

    def sync_out(self) -> None:
        try:
            setattr(self.model, self.model_key, self.type_(self._stringvar.get()))
            self.notify_change()
        except ValueError:
            # Tolerate temporarily invalid values
            pass

    def sync_in(self) -> None:
        val = getattr(self.model, self.model_key)
        self._stringvar.set(str(val))

    def _config_widget(self) -> None:
        self._stringvar = StringVar(self.parent)
        self.sync_in()
        self.configure(textvariable=self._stringvar, command=lambda: self.sync_out())
        self.bind('<KeyRelease>', lambda e: self.sync_out())
        if issubclass(self.type_, ConstrainedInt):
            tp: Type[ConstrainedInt] = self.type_
            self.configure(increment=1)
            if tp.gt is not None:
                self.configure(from_=tp.gt + 1)
            if tp.ge is not None:
                self.configure(from_=tp.ge)
            if tp.lt is not None:
                self.configure(to=tp.lt - 1)
            if tp.le is not None:
                self.configure(to=tp.le)
        elif issubclass(self.type_, ConstrainedFloat):
            tp: Type[ConstrainedFloat] = self.type_
            self.configure(increment=tp.multiple_of)
            if tp.gt is not None:
                self.configure(from_=tp.gt)
            if tp.ge is not None:
                self.configure(from_=tp.ge)
            if tp.lt is not None:
                self.configure(to=tp.lt)
            if tp.le is not None:
                self.configure(to=tp.le)
        elif issubclass(self.type_, float):
            raise TypeError(f'Please use ConstrainedFloat for {self.model_key}')
        elif issubclass(self.type_, int):
            raise TypeError(f'Please use ConstrainedInt for {self.model_key}')
        else:
            print(f'Unknown type f{repr(self.type_)}')
