# Library Imports
import unittest
import wx

# Internal Imports
import pyappframework as pyaf
from pyappframework import ui
from pyappframework.ui import controls as ctl

class TestWindow(ui.Window):
    def __init__(self, *args, **kw):
        self.bool_var = pyaf.Mutable[bool](False)
        self.str_var = pyaf.Mutable[str]("")
        self.str_var2 = pyaf.Mutable[str]("")
        self.image_var = pyaf.Mutable[wx.Image](wx.Image("test/resources/test_image.png", type=wx.BITMAP_TYPE_PNG).Rescale(50, 50))
        self.bitmap_var = pyaf.Mutable[wx.Bitmap](wx.Image("test/resources/test_image.png", type=wx.BITMAP_TYPE_PNG).Rescale(50, 50).ConvertToBitmap())
        super().__init__(*args, **kw)
        self.SetTitle("TestWindow")
        self.bool_var.value = True
        self.bool_var.addListener(self.onCheckBoxValueChange)

    def body(self) -> ctl.Panel:
        return (
            ctl.ScrollablePanel(wx.BoxSizer(wx.VERTICAL))
            .body [[
                ctl.StaticText(label="StaticText")
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.CheckBox(value=self.bool_var, label="CheckBox")
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.CheckBox(value=self.bool_var, label=self.str_var2)
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.StaticText(label=self.str_var)
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.StaticLine()
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.StaticBitmap(image=wx.Image("test/resources/test_image.png", type=wx.BITMAP_TYPE_PNG).Rescale(50, 50).ConvertToBitmap())
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.StaticBitmap(image=wx.Image("test/resources/test_image.png", type=wx.BITMAP_TYPE_PNG).Rescale(50, 50))
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.StaticBitmap(image=self.image_var)
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.StaticBitmap(image=self.bitmap_var)
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.Button(label="Button")
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.TextCtrl(value=self.str_var2)
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.Gauge()
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.TreeCtrl()
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.DataViewCtrl()
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.SearchCtrl(value=self.str_var2)
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.InfoBar()
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.SplitterWindow(ori=ctl.Orientation.VERTICAL)
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.ListBox()
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.Choice()
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT)),
                ctl.WebView()
                    .sizer(wx.SizerFlags().Border(wx.TOP | wx.LEFT))
            ]]
        )

    @pyaf.event_handler
    def onCheckBoxValueChange(self, evt: pyaf.MutationEvent):
        self.str_var.value = "True" if evt.newValue else "False"

class ControlsTest(unittest.TestCase):
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
