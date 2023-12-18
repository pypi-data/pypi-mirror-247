# Library Imports
import wx
from typing import Optional

# Internal Imports
from .menubar import MenuBar
from ..view import View

class Dialog(wx.Dialog, View):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, None, *args, **kw)
        View.__init__(self)
        self.setWxInstance(self)
        self.initialize(self, self)

        menubar = self.menubar()
        if menubar is not None:
            menubar.initialize(self)

    def menubar(self) -> Optional[MenuBar]:
        pass
