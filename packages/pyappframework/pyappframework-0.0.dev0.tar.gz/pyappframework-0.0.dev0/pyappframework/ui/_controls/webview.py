# Library Imports
import wx
import wx.html2 as wh
from typing import Optional

# Internal Imports
from ..view import PrimitiveView
from .control import Control

class WebView(Control):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        wv = wh.WebView.New(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        return wv
