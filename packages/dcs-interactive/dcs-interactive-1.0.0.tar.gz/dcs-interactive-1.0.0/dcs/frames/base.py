#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from tkinter import ttk, Tk, Toplevel, BOTH
from typing import Type, List


class Group:
    NAME: str


class BaseFrame(ttk.Frame):
    pass


class Window:
    GROUP: Type[Group]
    TITLE: str
    FRAME: Type[BaseFrame]

    @classmethod
    def make_title(cls) -> str:
        return f'{cls.GROUP.NAME} - {cls.TITLE}'

    @classmethod
    def make_frame(cls, root) -> ttk.Frame:
        frm = cls.FRAME(root)
        frm.pack(expand=True, fill=BOTH)
        return frm

    @classmethod
    def make_window(cls, root) -> Toplevel:
        win = Toplevel(root)
        win.title(cls.make_title())
        cls.make_frame(win)
        return win

    @classmethod
    def main(cls):
        logging.basicConfig(level=logging.INFO)

        root = Tk()
        root.title(cls.make_title())
        cls.make_frame(root)
        root.mainloop()


def get_groups(win_cls: List[Type[Window]]) -> List[Type[Group]]:
    grp_cls: List[Type[Group]] = []
    for win in win_cls:
        if win.GROUP not in grp_cls:
            grp_cls.append(win.GROUP)
    return list(sorted(grp_cls, key=lambda grp: grp.NAME))


def get_win_of_group(win_cls: List[Type[Window]], grp: Type[Group]) -> List[Type[Window]]:
    return list(filter(lambda win: win.GROUP == grp, win_cls))
