#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import unittest
from typing import List
from pydantic import BaseModel

from dcs.config.store import Store, ConfigObject


class ExampleSub(BaseModel):
    id: int
    title: str


class ExampleConfig(ConfigObject):
    _KEY = 'example'
    id: int
    name: str
    sub: List[ExampleSub]


class StoreTest(unittest.TestCase):
    def test_deserialize(self):
        in_data = {
            'example': {
                'id': 1,
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

        cfg = store.get_config(ExampleConfig)
        self.assertEqual(ExampleConfig, type(cfg))
        self.assertEqual(2, len(cfg.sub))
        self.assertEqual(ExampleSub, type(cfg.sub[0]))
        self.assertEqual(ExampleSub, type(cfg.sub[1]))

        sub0 = cfg.sub[0]
        self.assertEqual(id(cfg.sub[0]), id(sub0))

        self.assertEqual(id(cfg), id(store.get_config(ExampleConfig)))

        self.assertEqual(in_data, store.dump_obj())
