# Library Imports
import wx
from typing_extensions import Self
import abc

# Internal Imports
from .attribute import AttributeContainer

class PrimitiveView(AttributeContainer[wx.Window, wx.Window, wx.Window]):
    def __init__(self):
        super().__init__()
        self.__wx_instance = None

    def initialize(self, root: Self, parent: Self) -> wx.Window:
        self.__wx_instance = self._initialize(root, parent)
        self.runAttribDelegates(root.getWxInstance(), parent.getWxInstance(), self.__wx_instance)
        return self.__wx_instance

    def setWxInstance(self, instance: wx.Window):
        self.__wx_instance = instance
    
    def getWxInstance(self) -> wx.Window:
        assert self.__wx_instance is not None
        return self.__wx_instance

    @abc.abstractmethod
    def _initialize(self, root: Self, parent: Self) -> wx.Window:
        pass

class View(PrimitiveView):
    def __init__(self):
        super().__init__()
        self.__body = self.body()
    
    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        return self.__body.initialize(root, parent)

    @abc.abstractmethod
    def body(self) -> PrimitiveView:
        pass
