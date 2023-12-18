# Library Imports
import wx
from typing import Optional
import abc

# Internal Imports
from .menubar import Menu
from .view import View

class Window(wx.Frame, View):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, None, *args, **kw)
        View.__init__(self)
        self.setWxInstance(self)
        self.initialize(self, self)

        mbitems = self.menubar()
        if mbitems is not None:
            menubar = wx.MenuBar()
            for item in mbitems:
                item.initialize(menubar, None)

    def menubar(self) -> Optional[list[Menu]]:
        pass
