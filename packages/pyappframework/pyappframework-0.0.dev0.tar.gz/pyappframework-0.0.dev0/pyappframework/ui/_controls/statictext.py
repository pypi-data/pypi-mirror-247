# Library Imports
import wx
from typing import Optional

# Internal Imports
from ..view import PrimitiveView
from .control import Control
from ...mutable import MutableValue, valueof, ismutable

class StaticText(Control):
    def __init__(self, label: MutableValue[str]):
        super().__init__()
        self.label = label

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        st = wx.StaticText(parent.getWxInstance())
        st.SetLabelText(valueof(self.label))
        if ismutable(self.label):
            self.label.syncTo(st.SetLabel)
        return st
