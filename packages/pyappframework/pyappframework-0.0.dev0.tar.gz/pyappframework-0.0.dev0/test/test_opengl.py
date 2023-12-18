# Library Imports
import unittest
import wx
from OpenGL import GL as gl
from wx import glcanvas as wxgl

# Internal Imports
from pyappframework import ui
from pyappframework.ui import controls as ctl
from pyappframework.ui._controls import glcanvas as glc
from pyappframework.decorators import event_handler

class TestGLView(glc.GLView):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw, attribList=(wxgl.WX_GL_RGBA, wxgl.WX_GL_DOUBLEBUFFER, wxgl.WX_GL_DEPTH_SIZE, 24))
        self.__size = None

    def OnGLInit(self, canvas: wxgl.GLCanvas, ctx: wxgl.GLContext):
        gl.glClearColor(0, 0, 0, 1)

    def OnPaint(self, canvas: wxgl.GLCanvas, ctx: wxgl.GLContext):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glColor(1, 0, 0)
        gl.glVertex(-.2886, -.25)
        gl.glColor(0, 1, 0)
        gl.glVertex(.2886, -.25)
        gl.glColor(0, 0, 1)
        gl.glVertex(0, .25)
        gl.glEnd()
        canvas.SwapBuffers()

    def OnResize(self, canvas: wxgl.GLCanvas, ctx: wxgl.GLContext, size: wx.Size):
        if size.width <= 0 or size.height <= 0:
            return
        if self.__size is None:
            self.__size = size
        gl.glViewport(0, 0, size.width, size.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(
            -(size.width / self.__size[0] / 2),
            (size.width / self.__size[0] / 2),
            -(size.height / self.__size[1] / 2),
            (size.height / self.__size[1] / 2),
            -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

class TestWindow(ui.Window):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.SetTitle("TestWindow")

    def body(self) -> ctl.Panel:
        return (
            ctl.Panel(wx.BoxSizer(wx.VERTICAL))
            .body [[
                TestGLView()
                    .sizer(proportion=1, flag=wx.EXPAND)
            ]]
        )

class OpenGLTest(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.frame = None

    def tearDown(self):
        wx.CallAfter(self.app.ExitMainLoop)
        self.app.MainLoop()
        assert self.frame is not None
        self.frame.Destroy()
        self.app.Destroy()

    def runTest(self):
        self.frame = TestWindow()
        self.frame.Show()
