#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unittest
from typing import List
from pydantic import conint, confloat
from tkinter import Tk, ttk
from enum import IntEnum
import toml

from dcs.config.store import Store, ConfigObject, ConfigControlFrame
from dcs.config.ui import ui_create


class ExampleSubFrame(ConfigControlFrame):
    wdg_id: ttk.Spinbox
    wdg_title: ttk.Entry


@ui_create
class ExampleSub(ConfigObject):
    id: conint(ge=0, lt=10000) = 1
    title: str = 'test'

    def make_config_widget(self, parent: ttk.Widget) -> ConfigControlFrame:
        frm = ExampleSubFrame(parent)
        frm.pack()
        ttk.Label(frm, text="Id:").grid(row=0, column=0)
        frm.wdg_id = self.ui_create_id(frm)
        frm.wdg_id.grid(row=0, column=1)
        ttk.Label(frm, text="Title:").grid(row=1, column=0)
        frm.wdg_title = self.ui_create_title(frm)
        frm.wdg_title.grid(row=1, column=1)
        return frm



class ExampleIntEnum(IntEnum):
    Option1 = 1
    Option2 = 2


@ui_create
class ExampleConfig(ConfigObject):
    _KEY = 'example'
    id: conint(ge=0, lt=10) = 1
    name: str = 'Hello'
    sub: List[ExampleSub] = [
        ExampleSub(id=1, title='item 1'),
        ExampleSub(id=2, title='item 2'),
    ]
    int_option: ExampleIntEnum = ExampleIntEnum.Option2
    flt: confloat(ge=0.0, lt=10.0, multiple_of=0.01) = 0.12


class UITest(unittest.TestCase):
    def test_deserialize(self):
        in_data = {
            'example': {
                'id': 0,
                'name': 'Test1',
                'sub': [
                    {
                        'id': 0,
                        'title': 'Title1',
                    },
                    {
                        'id': 1,
                        'title': 'Title2',
                    },
                ]
            }
        }

        loaded_store = Store.load_obj(in_data, 'default')

        store = Store.get_instance('default')
        self.assertEqual(id(loaded_store), id(store))

        cfg: ExampleConfig = store.get_config(ExampleConfig)
        self.assertIn('ui_create_id', dir(cfg))


class UIInteractiveTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Tk()
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.pack()

        self.store = Store.new('default')

    def _print_cfg(self) -> None:
        print(repr(self.store.get_config(ExampleConfig)))
        print(toml.dumps(self.store.dump_obj()))
        #print(self.store.get_config(ExampleConfig).json())

    def _run_ui(self) -> bool:
        self.res = False

        def act(ok: bool) -> None:
            self.root.destroy()
            self.res = ok

        self.ok_btn = ttk.Button(self.root, text='Test OK', command=lambda: act(True))
        self.ok_btn.pack()
        self.ok_fail = ttk.Button(self.root, text='Test Fail', command=lambda: act(False))
        self.ok_fail.pack()

        self.root.mainloop()

        return self.res

    def test_int_widget(self):
        cfg = self.store.get_config(ExampleConfig)
        wdg = cfg.ui_create_id(self.frm)
        wdg.pack()
        wdg.listen_change(lambda x, y, z: self._print_cfg())

        self.assertTrue(self._run_ui())

    def test_float_widget(self):
        cfg = self.store.get_config(ExampleConfig)
        wdg = cfg.ui_create_flt(self.frm)
        wdg.pack()
        wdg.listen_change(lambda x, y, z: self._print_cfg())

        self.assertTrue(self._run_ui())

    def test_dropdown_widget(self):
        cfg = self.store.get_config(ExampleConfig)
        wdg = cfg.ui_create_int_option_dropdown(self.frm)
        wdg.pack()
        wdg.listen_change(lambda x, y, z: self._print_cfg())

        self.assertTrue(self._run_ui())

    def test_list_widget(self):
        cfg = self.store.get_config(ExampleConfig)
        wdg = cfg.ui_create_sub_list(self.frm, lambda e: e.title)
        wdg.pack()
        wdg.listen_change(lambda x, y, z: self._print_cfg())

        self.assertTrue(self._run_ui())
