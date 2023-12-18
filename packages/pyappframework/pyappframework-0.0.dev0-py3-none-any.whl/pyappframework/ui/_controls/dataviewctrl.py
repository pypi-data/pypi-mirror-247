# Library Imports
import wx
from wx import dataview as dv
from typing import Optional

# Internal Imports
from ..view import PrimitiveView
from .control import Control
from ...decorators import chainable
from .. import attribute as attr

class DataViewCtrl(Control):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)
        self.model = attr.TypedAttribute[wx.Window, wx.Window, wx.Window, dv.DataViewModel](self)

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        dvc = dv.DataViewCtrl(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        model = self.model.getTypedValue()
        if model is not None:
            dvc.AssociateModel(model)
        return dvc
