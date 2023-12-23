#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.


from tkinter import ttk, StringVar

from .base import make_config_widget_base


class StrWidget(make_config_widget_base(ttk.Entry)):
    MODEL_TYPE = str

    def sync_out(self) -> None:
        try:
            setattr(self.model, self.model_key, self._stringvar.get())
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
        self.configure(textvariable=self._stringvar)
        self.bind('<KeyRelease>', lambda e: self.sync_out())
