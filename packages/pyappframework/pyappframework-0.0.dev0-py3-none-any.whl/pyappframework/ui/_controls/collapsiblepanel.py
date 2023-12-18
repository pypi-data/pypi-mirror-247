# Library Imports
import wx
from typing import Optional

# Internal Imports
from .control import Control
from .. import attribute as attr
from ..view import PrimitiveView

class CollapsiblePanel(Control):
    def __init__(self, sizer: wx.Sizer, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)
        self.__sizer = sizer
        self.body = attr.BodyAttribute(self)

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        cp = wx.CollapsiblePane(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        panel = cp.GetPane()
        panel.SetSizer(self.__sizer)
        self.setWxInstance(panel)
        if isinstance(self.body.value, list):
            for view in self.body.value:
                assert isinstance(view, PrimitiveView)
                view.initialize(root, self)
        return cp
