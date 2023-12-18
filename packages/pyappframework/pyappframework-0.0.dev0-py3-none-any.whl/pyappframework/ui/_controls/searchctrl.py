# Library Imports
import wx
from typing import Optional

# Internal Imports
from ..view import PrimitiveView
from .control import Control
from ...mutable import Mutable

class SearchCtrl(Control):
    def __init__(self, value: Mutable[str]):
        super().__init__()
        self.value = value

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        sc = wx.SearchCtrl(parent.getWxInstance())
        root.getWxInstance().Bind(wx.EVT_TEXT, self.value.sync(sc.GetValue, sc.SetValue), sc)
        return sc
