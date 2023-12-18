# Library Imports
import wx
from typing import Optional

try:
    import matplotlib.backends.backend_wxagg as mpwx
except ImportError as ex:
    raise ImportError("Required dependency matplotlib is not present") from ex

# Internal Imports
from ..view import PrimitiveView
from .control import Control

class Plot(Control):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        tc = mpwx.FigureCanvasWxAgg(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        return tc
