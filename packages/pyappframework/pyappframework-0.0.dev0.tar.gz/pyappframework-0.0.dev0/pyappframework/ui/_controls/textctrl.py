# Library Imports
import wx
from typing import Optional

# Internal Imports
from ..view import PrimitiveView
from .control import Control
from ...mutable import Mutable

class TextCtrl(Control):
    def __init__(self, value: Mutable[str]):
        super().__init__()
        self.value = value

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        tc = wx.TextCtrl(parent.getWxInstance())
        root.getWxInstance().Bind(wx.EVT_TEXT, self.value.sync(tc.GetValue, tc.SetValue), tc)
        return tc

