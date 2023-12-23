#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from typing import Type, List, Callable, AnyStr, Optional
from tkinter import ttk, Listbox, X, LEFT, ACTIVE
from tkinter.simpledialog import Dialog
from pydantic import BaseModel
from ..store import ConfigObject

from .base import make_config_widget_base


Entry2StrCb = Callable[[ConfigObject], AnyStr]


class ListBoxWidget(make_config_widget_base(ttk.Frame)):
    MODEL_TYPE = list
    FLAVOUR = 'list'

    def __init__(self, model: BaseModel, model_key: str, tp: Type, parent, translate_cb: Entry2StrCb, *args, **kwargs):
        super().__init__(model, model_key, tp, parent, *args, **kwargs)

        self.translate_cb: Entry2StrCb = translate_cb

        self._box = Listbox(self)
        self._box.bind('<Double-Button-1>', self._on_double_click)
        self._box.pack(fill=X)

        self._add_btn = ttk.Button(self, text='+ Add', command=self._on_add)
        self._add_btn.pack(side=LEFT, padx=5, pady=5)

        self._remove_btn = ttk.Button(self, text='- Remove', command=self._on_remove)
        self._remove_btn.pack(side=LEFT, padx=5, pady=5)

        self._up_btn = ttk.Button(self, text='^ Up', command=self._on_up)
        self._up_btn.pack(side=LEFT, padx=5, pady=5)

        self._down_btn = ttk.Button(self, text='v Down', command=self._on_down)
        self._down_btn.pack(side=LEFT, padx=5, pady=5)

    def sync_out(self) -> None:
        self.notify_change()

    def sync_in(self) -> None:
        self._box.delete(0, self._box.size())

        l = getattr(self.model, self.model_key)
        for e in l:
            self._box.insert('end', self.translate_cb(e))

    def _config_widget(self):
        self.sync_in()

    def _run_dialog(self, index: Optional[int]):
        l: List[ConfigObject] = getattr(self.model, self.model_key)
        tp = self.type_

        class EditDialog(Dialog):
            def __init__(self, index, *args, **kwargs):
                self.index = index
                super().__init__(*args, **kwargs)

            def body(self, master) -> None:
                if self.index is not None:
                    self.item = None
                    w = l[self.index].make_config_widget(master)
                else:
                    self.item = tp()
                    w = self.item.make_config_widget(master)
                w.pack()

            def buttonbox(self):
                box = ttk.Frame(self)

                w = ttk.Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
                w.pack(side=LEFT, padx=5, pady=5)

                self.bind("<Return>", self.ok)

                if self.index is None:
                    w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
                    w.pack(side=LEFT, padx=5, pady=5)

                    self.bind("<Escape>", self.cancel)

                box.pack()

            def apply(self):
                if self.index is None:
                    l.append(self.item)

        EditDialog(index, self)
        setattr(self.model, self.model_key, l)
        self.notify_change()
        self.sync_in()

    def _on_add(self):
        self._run_dialog(None)

        last = len(getattr(self.model, self.model_key))
        self._box.selection_set(last - 1)
        self._box.see(last - 1)
        self._box.activate(last - 1)
        self._box.selection_anchor(last - 1)

    def _on_double_click(self, _):
        index = self._box.curselection()
        if len(index) > 0:
            self._run_dialog(index[0])

    def _on_remove(self):
        l: List[ConfigObject] = getattr(self.model, self.model_key)

        index = self._box.curselection()
        if len(index) > 0:
            l.pop(index[0])

            setattr(self.model, self.model_key, l)
            self.notify_change()
            self.sync_in()

            self._box.selection_set(index[0] - 1)
            self._box.see(index[0] - 1)
            self._box.activate(index[0] - 1)
            self._box.selection_anchor(index[0] - 1)

    def _on_up(self):
        l: List[ConfigObject] = getattr(self.model, self.model_key)

        index = self._box.curselection()
        if len(index) > 0 and index[0] > 0:
            l.insert(index[0] - 1, l.pop(index[0]))

            setattr(self.model, self.model_key, l)
            self.sync_in()
            self.notify_change()

            self._box.selection_set(index[0] - 1)
            self._box.see(index[0] - 1)
            self._box.activate(index[0] - 1)
            self._box.selection_anchor(index[0] - 1)

    def _on_down(self):
        l: List[ConfigObject] = getattr(self.model, self.model_key)

        index = self._box.curselection()
        if len(index) > 0 and index[0] < len(l):
            l.insert(index[0] + 1, l.pop(index[0]))

            setattr(self.model, self.model_key, l)
            self.sync_in()
            self.notify_change()
            self._box.selection_set(index[0] + 1)
            self._box.see(index[0] + 1)
            self._box.activate(index[0] + 1)
            self._box.selection_anchor(index[0] + 1)
