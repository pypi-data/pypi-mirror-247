# Library Imports
import wx

# Internal Imports
from .control import Control
from ...mutable import Mutable, MutableValue, valueof, ismutable
from ..view import PrimitiveView
from .. import attribute as attr

class CheckBox(Control):
    def __init__(self, value: Mutable[bool], label: MutableValue[str]):
        super().__init__()
        self.value = value
        self.label = label

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        cb = wx.CheckBox(parent.getWxInstance())
        cb.SetLabel(valueof(self.label))
        cb.SetValue(valueof(self.value))
        if ismutable(self.label):
            root.getWxInstance().Bind(wx.EVT_CHECKBOX, self.label.sync(cb.GetLabelText, cb.SetLabelText), cb)
        root.getWxInstance().Bind(wx.EVT_CHECKBOX, self.value.sync(cb.GetValue, cb.SetValue), cb)
        return cb
