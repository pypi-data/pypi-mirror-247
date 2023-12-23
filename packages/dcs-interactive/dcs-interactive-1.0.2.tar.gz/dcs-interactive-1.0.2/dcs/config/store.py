#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import toml
import json
from typing import Dict, AnyStr, Callable, Type, Any, Optional, List
from pydantic import BaseModel, PrivateAttr
import appdirs
import os
import logging
from tkinter import ttk
from abc import abstractmethod, ABC


class ConfigControlFrame(ttk.Frame):
    ctrl_widgets: List[ttk.Widget]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctrl_widgets = []

    def add_widget(self, w: ttk.Widget) -> None:
        self.ctrl_widgets.append(w)

    def widgets_on_change(self, cb) -> None:
        for w in self.ctrl_widgets:
            w.listen_change(cb)


class ConfigObject(BaseModel, ABC):
    _KEY: AnyStr = PrivateAttr()

    @classmethod
    def get_key(cls) -> AnyStr:
        return cls._KEY

    @abstractmethod
    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        ...


class Store:
    __instances: Dict[str, Store] = {}

    def __init__(self, raw_objs: Dict[AnyStr, Any], save_cb: Optional[Callable[[Store], None]] = None):
        self._raw_objs: Dict[AnyStr, Any] = raw_objs
        self._cfg_objs: Dict[AnyStr, ConfigObject] = {}
        self._save_cb: Optional[Callable[[Store], None]] = save_cb

    @staticmethod
    def get_instance(name: str = 'default') -> Store:
        if name in Store.__instances:
            return Store.__instances[name]
        else:
            raise KeyError(f'The Store instance {name} does not exist.')

    @classmethod
    def load_obj(cls, obj: Dict[AnyStr, Any], name: str = 'default', *args, **kwargs) -> Store:
        if name not in Store.__instances:
            Store.__instances[name] = cls(obj, *args, **kwargs)
            return Store.__instances[name]
        else:
            raise KeyError(f'The Store instance {name} already exists.')

    @classmethod
    def new(cls, name: str = 'default', *args, **kwargs) -> Store:
        if name not in Store.__instances:
            Store.__instances[name] = cls({}, *args, **kwargs)
            return Store.__instances[name]
        else:
            raise KeyError(f'The Store instance {name} already exists.')

    def dump_obj(self) -> Dict[AnyStr, Any]:
        obj: Dict[AnyStr, Any] = self._raw_objs
        for key, item in self._cfg_objs.items():
            obj[key] = json.loads(item.json())
        return obj

    def get_config(self, tp: Type[ConfigObject]):
        key = tp.get_key()
        if key not in self._cfg_objs:
            if key in self._raw_objs:
                self._cfg_objs[key] = tp.parse_obj(self._raw_objs[key])
            else:
                self._cfg_objs[key] = tp()
        return self._cfg_objs[key]

    def save(self) -> None:
        if self._save_cb is not None:
            self._save_cb(self)


class TomlStore(Store):
    def __init__(self, raw_objs: Dict[AnyStr, Any], toml_file: str):
        super().__init__(raw_objs, save_cb=self._do_save)
        self.toml_file: str = toml_file

    @classmethod
    def load_or_create_toml(cls, toml_file: str, name: str = 'default') -> TomlStore:
        try:
            s = Store.get_instance(name)
        except KeyError:
            try:
                s = TomlStore.load_toml(toml_file, name)
                logging.info(f'Loaded config from {toml_file}')
            except FileNotFoundError:
                s = TomlStore.new(name, toml_file=toml_file)
                logging.info(f'New config at {toml_file}')
        return s

    @classmethod
    def load_toml(cls, toml_file: str, name: str = 'default') -> TomlStore:
        obj = toml.load(toml_file)
        return TomlStore.load_obj(obj, name, toml_file=toml_file)

    def dump_toml(self) -> None:
        base_dir = os.path.dirname(self.toml_file)
        if not os.path.exists(base_dir):
            logging.info(f'Creating directory {base_dir}')
            os.mkdir(base_dir)
        with open(self.toml_file, 'w', encoding='utf-8') as f:
            toml.dump(self.dump_obj(), f)

    def _do_save(self, s: Store) -> None:
        assert id(self) == id(s)
        self.dump_toml()


DEFAULT_PATH = os.path.join(
    appdirs.user_config_dir('dcs_interactive', 'Philipp Le'),
    'config.toml'
)


def default_store() -> TomlStore:
    return TomlStore.load_or_create_toml(DEFAULT_PATH, 'default')

