# Library Imports
import unittest
import wx

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
        )

    def menubar(self) -> list[ui.Menu]:
        return [
            ui.Menu(title="Menu1")
                .body [[
                ui.MenuItem(wx.ID_ANY, "MenuItem1"),
                ui.MenuItem(wx.ID_ANY, "MenuItem2"),
                ui.MenuItem(wx.ID_ANY, "MenuItem3"),
                ui.MenuSeparator(),
                ui.MenuItem(wx.ID_ANY, "MenuItem4"),
                ui.MenuItem(wx.ID_ANY, "MenuItem5"),
                ui.MenuItem(wx.ID_ANY, "MenuItem6"),
            ]],
            ui.Menu(title="Menu2")
            .body [[
                ui.MenuItem(wx.ID_ANY, "MenuItem1"),
                ui.Menu("SubMenu1")
                .body [[
                    ui.MenuItem(wx.ID_ANY, "MenuItem4"),
                    ui.MenuItem(wx.ID_ANY, "MenuItem5"),
                    ui.MenuItem(wx.ID_ANY, "MenuItem6"),
                ]],
            ]],
            ui.Menu(title="Menu3"),
        ]


class WindowTest(unittest.TestCase):
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
