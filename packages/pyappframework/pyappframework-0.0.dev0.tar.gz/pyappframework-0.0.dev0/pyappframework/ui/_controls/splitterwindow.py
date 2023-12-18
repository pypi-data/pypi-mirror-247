# Library Imports
import wx
from typing import Tuple
from enum import Enum
from typing import Optional

# Internal Imports
from .. import attribute as attr
from ..view import PrimitiveView
from .control import Control

class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1

class SplitterWindow(Control):
    def __init__(self, ori: Orientation, pos: int = 0, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)
        self.__ori = ori
        self.__pos = pos
        self.body = attr.BodyAttribute(self)

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        contents = self.body.value
        sw = wx.SplitterWindow(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        self.setWxInstance(sw)
        instance = []
        if isinstance(contents, list) and len(contents) == 2:
            for view in contents:
                assert isinstance(view, PrimitiveView)
                instance.append(view.initialize(root, self))
            if self.__ori == Orientation.HORIZONTAL:
                sw.SplitHorizontally(instance[0], instance[1], self.__pos)
            else:
                sw.SplitVertically(instance[0], instance[1], self.__pos)
        return sw
