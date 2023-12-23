#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dcs.frames import get_groups, get_win_of_group
from dcs.frames.base import Group, Window
import logging
from tkinter import ttk, Tk, BOTTOM, BOTH
from typing import Type, Dict, Any
import webbrowser


class MainWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wdg_treeview = ttk.Treeview(self)
        self.wdg_treeview.pack(expand=True, fill=BOTH)
        self.wdg_treeview.bind('<Double-Button-1>', self._on_double_click)

        self.group_ids: Dict[Type[Group], Any] = {}
        self.win_ids: Dict[Type[Window], Any] = {}
        for grp in get_groups():
            self.group_ids[grp] = self.wdg_treeview.insert('', 'end', None, text=grp.NAME)
            for win in get_win_of_group(grp):
                self.win_ids[win] = self.wdg_treeview.insert(self.group_ids[grp], 'end', None, text=win.TITLE)

        self.frm_copyright = ttk.Frame(self, height=35)
        self.frm_copyright.pack(side=BOTTOM, expand=False)
        ttk.Label(self.frm_copyright, text='Copyright (c) 2022 Philipp Le').pack()
        self.wdg_license = ttk.Button(self.frm_copyright, text='Mozilla Public License v2.0',
                                      command=self._view_license)
        self.wdg_license.pack()

    def find_win(self, iid) -> Type[Window]:
        for win, win_iid in self.win_ids.items():
            if win_iid == iid:
                return win
        raise KeyError

    def _on_double_click(self, event):
        item_id = event.widget.focus()
        try:
            win = self.find_win(item_id)
            win.make_window(self)
        except KeyError:
            pass

    def _view_license(self):
        webbrowser.open('https://mozilla.org/MPL/2.0/', new=1)


def main():
    logging.basicConfig(level=logging.INFO)

    root = Tk()
    root.title('Digital Communication Systemes - Interactive')
    root.geometry('800x600')
    win = MainWindow(root)
    win.pack(expand=True, fill=BOTH)
    root.mainloop()


if __name__ == '__main__':
    main()
