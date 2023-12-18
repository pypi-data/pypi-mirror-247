# Library Imports
import wx
from typing import Any, Optional, Callable, TypeVar
import abc

# Internal Imports
from ..view import PrimitiveView
from .control import Control
from ...decorators import chainable
from .. import attribute as attr


class ToolBar(Control):
    def __init__(self, *args, **kw):
        super().__init__()
        self.body = attr.BodyAttribute[wx.Window, wx.Window, wx.Window, Tool](self)
        self.__init_args = (args, kw)

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        tb = wx.ToolBar(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        self.setWxInstance(tb)
        assert isinstance(self.body.value, list)
        for tool in self.body.value:
            assert isinstance(tool, Tool)
            tool.initialize(root, self)
        tb.Realize()
        return tb

class Tool(attr.AttributeContainer[wx.Window, ToolBar, wx.ToolBarToolBase]):
    def __init__(self):
        super().__init__()
        self.__wx_instance = None

    def initialize(self, root: PrimitiveView, parent: ToolBar) -> wx.ToolBarToolBase:
        self.__wx_instance = self._initialize(root, parent)
        self.runAttribDelegates(root.getWxInstance(), parent, self.__wx_instance)
        return self.__wx_instance

    @abc.abstractmethod
    def _initialize(self, root: PrimitiveView, parent: ToolBar) -> wx.ToolBarToolBase:
        pass

class NormalTool(Tool):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)

    def _initialize(self, root: PrimitiveView, parent: ToolBar) -> wx.ToolBarToolBase:
        instance = parent.getWxInstance()
        assert isinstance(instance, wx.ToolBar)
        tool = instance.AddTool(*self.__init_args[0], **self.__init_args[1])
        return tool

class RadioTool(Tool):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)

    def _initialize(self, root: PrimitiveView, parent: ToolBar) -> wx.ToolBarToolBase:
        instance = parent.getWxInstance()
        assert isinstance(instance, wx.ToolBar)
        tool = instance.AddRadioTool(*self.__init_args[0], **self.__init_args[1])
        return tool

class ControlTool(Tool):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)

    @chainable
    def control(self, c: PrimitiveView, /):
        self.__control = c

    def _initialize(self, root: PrimitiveView, parent: ToolBar) -> wx.ToolBarToolBase:
        assert isinstance(self.__control, PrimitiveView)
        ctrl = self.__control.initialize(root, parent)
        assert isinstance(ctrl, wx.Window)
        instance = parent.getWxInstance()
        assert isinstance(instance, wx.ToolBar)
        tool = instance.AddControl(ctrl, *self.__init_args[0], **self.__init_args[1])
        return tool

class ToolSeparator(Tool):
    def _initialize(self, root: PrimitiveView, parent: ToolBar) -> wx.ToolBarToolBase:
        instance = parent.getWxInstance()
        assert isinstance(instance, wx.ToolBar)
        tool = instance.AddSeparator()
        return tool

class ToolSpacer(Tool):
    def _initialize(self, root: PrimitiveView, parent: ToolBar) -> wx.ToolBarToolBase:
        instance = parent.getWxInstance()
        assert isinstance(instance, wx.ToolBar)
        tool = instance.AddStretchableSpace()
        return tool
