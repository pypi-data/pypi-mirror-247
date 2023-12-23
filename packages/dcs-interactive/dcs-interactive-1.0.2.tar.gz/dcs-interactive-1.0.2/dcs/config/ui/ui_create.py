#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Type, List, Dict, Optional
from pydantic import BaseModel

from .base import ConfigWidget
from .num_widget import NumWidget
from .str_widget import StrWidget
from .enum_widget import EnumDropdownWidget
from .list_widget import ListBoxWidget


_CLASS_REGISTRY: List[Type[ConfigWidget]] = [
    NumWidget,
    StrWidget,
    EnumDropdownWidget,
]


def _find_widget_classes(tp: Type, is_list: bool = False) -> Dict[Optional[str], Type[ConfigWidget]]:
    widget_classes: Dict[Optional[str], Type[ConfigWidget]] = {}
    if is_list:
        widget_classes[ListBoxWidget.FLAVOUR] = ListBoxWidget
    else:
        for cls in _CLASS_REGISTRY:
            if issubclass(tp, cls.MODEL_TYPE):
                widget_classes[cls.FLAVOUR] = cls
    if len(widget_classes) == 0:
        raise TypeError(f'No widget class for {repr(tp)} found.')
    return widget_classes


def _add_ui_create(model_cls: BaseModel, tp: Type[int], name: str, widget_type: Type[ConfigWidget],
                   flavour: Optional[str]):
    suffix = f'_{flavour}' if flavour is not None else ''
    setattr(model_cls, f'ui_create_{name}{suffix}', widget_type.make_ui_create_method(tp, name))


def ui_create(cls: BaseModel):
    for field in cls.__fields__.values():
        name = field.name
        tp = field.type_
        is_list = isinstance(field.default, list)
        try:
            widget_classes = _find_widget_classes(tp, is_list)
            for flavour, wgd_cls in widget_classes.items():
                _add_ui_create(cls, tp, name, wgd_cls, flavour)
        except TypeError as e:
            print(e)
    return cls
