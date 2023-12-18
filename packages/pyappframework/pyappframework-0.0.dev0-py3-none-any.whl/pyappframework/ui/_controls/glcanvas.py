# Library Imports
import wx
from typing import Optional
from abc import ABCMeta, abstractmethod

try:
    from OpenGL import GL as gl
    from wx import glcanvas as wxgl
except ImportError as ex:
    raise ImportError("Required dependency OpenGL is not present") from ex

# Internal Imports
from ..view import PrimitiveView
from .. import attribute as attr
from .control import Control
from ...decorators import chainable, event_handler

class GLView(Control):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)
        self.contextArgs = attr.ArgumentAttribute[wx.Window, wx.Window, wx.Window](self)
        self.__context = None
        self.__initialized = False

    def _initialize(self, root: PrimitiveView, parent: PrimitiveView) -> wx.Window:
        glc = wxgl.GLCanvas(parent.getWxInstance(), *self.__init_args[0], **self.__init_args[1])
        contextArgs = self.contextArgs.getArgs()
        self.__context = wxgl.GLContext(glc, None, *contextArgs[0], **contextArgs[1])
        glc.Bind(wx.EVT_ERASE_BACKGROUND, self._OnErase)
        glc.Bind(wx.EVT_SIZE, self._OnResize)
        glc.Bind(wx.EVT_PAINT, self._OnPaint)
        return glc

    def getContext(self) -> Optional[wxgl.GLContext]:
        return self.__context

    @abstractmethod
    def OnGLInit(self, canvas: wxgl.GLCanvas, ctx: wxgl.GLContext):
        pass

    @abstractmethod
    def OnPaint(self, canvas: wxgl.GLCanvas, ctx: wxgl.GLContext):
        pass

    @abstractmethod
    def OnResize(self, canvas: wxgl.GLCanvas, ctx: wxgl.GLContext, size: wx.Size):
        pass

    def _OnErase(self, evt: wx.Event):
        pass

    @event_handler
    def _OnPaint(self, evt: wx.Event):
        canvas = self.getWxInstance()
        context = self.getContext()
        assert isinstance(canvas, wxgl.GLCanvas) and isinstance(context, wxgl.GLContext)
        canvas.SetCurrent(context)
        if not self.__initialized:
            self.OnGLInit(canvas, context)
            self.__initialized = True
        self.OnPaint(canvas, context)

    @event_handler
    def _OnResize(self, evt: wx.Event):
        canvas = self.getWxInstance()
        context = self.getContext()
        assert isinstance(canvas, wxgl.GLCanvas) and isinstance(context, wxgl.GLContext)
        canvas.SetCurrent(context)
        size = canvas.GetClientSize()
        self.OnResize(canvas, context, size)
        canvas.Refresh(False)
