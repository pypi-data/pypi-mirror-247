# Library Imports
import wx
from typing import Optional

# Internal Imports
from .. import attribute as attr
from ..view import PrimitiveView
from .control import Control

class Notebook(Control):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)
        self.body = attr.BodyAttribute(self)

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        nb = wx.Notebook(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        self.setWxInstance(nb)
        if isinstance(self.body.value, list):
            for view in self.body.value:
                assert isinstance(view, PrimitiveView)
                instance = view.initialize(root, self)
                assert instance is not None
                nb.AddPage(instance, instance.GetLabel())
        return nb
