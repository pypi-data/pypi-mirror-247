# Library Imports
import wx

# Internal Imports
from .control import Control
from ..view import PrimitiveView

class Button(Control):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        btn = wx.Button(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        return btn
