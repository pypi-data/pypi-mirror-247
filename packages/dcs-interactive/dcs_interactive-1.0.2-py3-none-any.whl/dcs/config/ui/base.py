#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Type, Callable, List, Optional
from tkinter import ttk
from pydantic import BaseModel


class ConfigWidget:
    MODEL_TYPE: Type
    FLAVOUR: Optional[str] = None

    def listen_change(self, cb: Callable[[BaseModel, str, ConfigWidget], None]) -> None:
        raise NotImplementedError

    def notify_change(self) -> None:
        raise NotImplementedError

    def sync_out(self) -> None:
        raise NotImplementedError

    def sync_in(self) -> None:
        raise NotImplementedError

    def set_value(self, val) -> None:
        raise NotImplementedError

    @classmethod
    def make_ui_create_method(cls, tp: Type, name: str):
        raise NotImplementedError

    def get_widget(self) -> ttk.Widget:
        raise NotImplementedError


def make_config_widget_base(base: Type[ttk.Widget]) -> Type[ttk.Widget, ConfigWidget]:
    # The Pythonic way for generics

    class ConfigWidgetBase(base, ConfigWidget):
        def __init__(self, model: BaseModel, model_key: str, tp: Type, parent, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            self.parent = parent
            self._listeners: List[Callable[[BaseModel, str, ConfigWidget], None]] = []
            self.model = model
            self.model_key = model_key
            self.type_ = tp

        def listen_change(self, cb: Callable[[BaseModel, str, ConfigWidget], None]) -> None:
            self._listeners.append(cb)

        def notify_change(self) -> None:
            for cb in self._listeners:
                cb(self.model, self.model_key, self)

        def sync_out(self) -> None:
            raise NotImplementedError

        def sync_in(self) -> None:
            raise NotImplementedError

        @classmethod
        def make_ui_create_method(cls, tp: Type, name: str):
            def create(self: BaseModel, parent, *args, **kwargs):
                widget = cls(self, name, tp, parent, *args, **kwargs)
                widget._config_widget()
                return widget
            return create

        def _config_widget(self) -> None:
            pass

        def get_widget(self) -> ttk.Widget:
            return self

    return ConfigWidgetBase
