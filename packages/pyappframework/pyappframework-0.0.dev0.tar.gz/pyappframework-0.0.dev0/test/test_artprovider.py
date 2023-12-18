# Library Imports
import unittest
import wx
import re

# Internal Imports
from pyappframework import ui
from pyappframework.ui import controls as ctl

class TestWindow(ui.Window):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.SetTitle("TestWindow")

    def body(self) -> ctl.Panel:
        return (
            ctl.Panel(wx.BoxSizer(wx.VERTICAL))
            .body [[
                ctl.StaticBitmap(image=wx.ArtProvider.GetBitmap(ui.ArtID("solid_image"), wx.ART_TOOLBAR, wx.Size(20, 20))),
                ctl.StaticBitmap(image=wx.ArtProvider.GetBitmap(ui.ArtID("solid_image", wx.Colour(0, 0, 0)), wx.ART_TOOLBAR, wx.Size(20, 20))),
                ctl.StaticBitmap(image=wx.ArtProvider.GetBitmap(ui.ArtID("solid_image", (0, 0, 0)), wx.ART_TOOLBAR, wx.Size(20, 20))),
                ctl.StaticBitmap(image=wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, wx.Size(20, 20))),
            ]]
        )

class TestArtProvider(ui.SVGArtProvider):
    def CreateBitmap(self, artid: str, client: str, size: wx.Size):
        return ui.SVGArtProvider.CreateBitmap(self, artid, client, size)

    def getIconPath(self, name: str) -> str:
        fmtgrp = re.search(r'^(\w+)_([\w-]+)', name)
        assert fmtgrp is not None
        icontype, iconname = fmtgrp.groups()
        return f"test/resources/icons_fontawesome/{icontype}/{iconname}.svg"

class ArtProviderTest(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        wx.ArtProvider.Push(TestArtProvider())
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
