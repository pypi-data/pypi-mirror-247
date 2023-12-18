# Library Imports
import wx
from typing import Union

# Internal Imports
from ..view import PrimitiveView
from .control import Control
from ...mutable import Mutable
from ... import MutableValue


class StaticBitmap(Control):
    def __init__(self, image: Union[MutableValue[wx.Image], MutableValue[wx.Bitmap]]):
        super().__init__()
        self.image = image

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        sb = wx.StaticBitmap(parent.getWxInstance())
        if isinstance(self.image, Mutable):
            if isinstance(self.image.value, wx.Image):
                self.image.syncTo(lambda img: sb.SetBitmap(img.ConvertToBitmap()))
            elif isinstance(self.image.value, wx.Bitmap):
                self.image.syncTo(sb.SetBitmap)
            else:
                raise AssertionError
        elif isinstance(self.image, wx.Image):
            sb.SetBitmap(self.image.ConvertToBitmap())
        elif isinstance(self.image, wx.Bitmap):
            sb.SetBitmap(self.image)
        else:
            raise AssertionError
        return sb
