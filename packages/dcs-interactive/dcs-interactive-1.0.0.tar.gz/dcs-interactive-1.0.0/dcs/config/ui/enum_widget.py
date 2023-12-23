#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from typing import Type
from tkinter import ttk, StringVar
from pydantic import BaseModel
from enum import Enum

from .base import make_config_widget_base


class EnumDropdownWidget(make_config_widget_base(ttk.OptionMenu)):
    MODEL_TYPE = Enum
    FLAVOUR = 'dropdown'

    def __init__(self, model: BaseModel, model_key: str, tp: Type, parent, *args, **kwargs):
        self._var = StringVar(parent)
        super().__init__(model, model_key, tp, parent, self._var, *args, **kwargs)

    def _get_choices(self):
        return [val for val in self.type_.__members__.values()]

    def _get_choices_str(self):
        return [str(val.value) for val in self._get_choices()]

    def sync_out(self) -> None:
        try:
            index = self._get_choices_str().index(self._var.get())
            val = self._get_choices()[index]
            setattr(self.model, self.model_key, val)
            self.notify_change()
        except ValueError:
            # Tolerate temporarily invalid values
            raise
            pass

    def sync_in(self) -> None:
        val = getattr(self.model, self.model_key)
        index = self._get_choices().index(val)
        choices = self._get_choices_str()
        self.set_menu(choices[index], *choices)

    def _config_widget(self):
        self._var.trace('w', lambda x, y, z: self.sync_out())
        self.sync_in()
