# Library Imports
import wx
from wx.lib import scrolledpanel as sp
from typing import Optional

# Internal Imports
from .. import attribute as attr
from ..view import PrimitiveView
from .control import Control

class ScrollablePanel(Control):
    def __init__(self, sizer: wx.Sizer, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)
        self.__sizer = sizer
        self.body = attr.BodyAttribute(self)

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        label = self.__init_args[1].pop("label", None)
        panel = sp.ScrolledPanel(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        if label is not None:
            panel.SetLabel(label)
        panel.SetupScrolling()
        panel.SetSizer(self.__sizer)
        self.setWxInstance(panel)
        if isinstance(self.body.value, list):
            for view in self.body.value:
                assert isinstance(view, PrimitiveView)
                view.initialize(root, self)
        return panel
