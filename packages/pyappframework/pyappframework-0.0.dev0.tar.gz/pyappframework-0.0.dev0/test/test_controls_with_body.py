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
            ctl.ScrollablePanel(wx.BoxSizer(wx.VERTICAL))
            .body [[
                ctl.ToolBar(style=wx.TB_HORIZONTAL | wx.TB_TEXT)
                    .sizer(proportion=1, flag=wx.EXPAND)
                    .body [[
                    ctl.NormalTool(wx.ID_ANY, "Tool1", wx.NullBitmap),
                    ctl.NormalTool(wx.ID_ANY, "Tool2", wx.Image("test/resources/test_image.png", type=wx.BITMAP_TYPE_PNG).Rescale(50, 50).ConvertToBitmap(), wx.NullBitmap, wx.ITEM_CHECK),
                    ctl.ToolSeparator(),
                    ctl.RadioTool(wx.ID_ANY, "Tool6", wx.Image("test/resources/test_image.png", type=wx.BITMAP_TYPE_PNG).Rescale(50, 50).ConvertToBitmap()),
                    ctl.RadioTool(wx.ID_ANY, "Tool7", wx.Image("test/resources/test_image.png", type=wx.BITMAP_TYPE_PNG).Rescale(50, 50).ConvertToBitmap()),
                    ctl.RadioTool(wx.ID_ANY, "Tool8", wx.Image("test/resources/test_image.png", type=wx.BITMAP_TYPE_PNG).Rescale(50, 50).ConvertToBitmap()),
                    ctl.ToolSpacer(),
                    ctl.ControlTool("Tool3")
                        .control(
                            ctl.Choice(choices=[f"Choice{n}" for n in range(6)])
                        ),
                ]],
                ctl.SplitterWindow(ori=ctl.Orientation.VERTICAL)
                    .sizer(proportion=1, flag=wx.EXPAND)
                    .body [[
                        ctl.StaticText(label="StaticText1"),
                        ctl.StaticText(label="StaticText2"),
                    ]],
                ctl.SplitterWindow(ori=ctl.Orientation.HORIZONTAL)
                    .sizer(proportion=1, flag=wx.EXPAND)
                    .body [[
                        ctl.StaticText(label="StaticText1"),
                        ctl.StaticText(label="StaticText2"),
                    ]],
                ctl.SplitterWindow(ori=ctl.Orientation.HORIZONTAL)
                    .sizer(proportion=1, flag=wx.EXPAND),
                ctl.Notebook()
                    .sizer(proportion=1, flag=wx.EXPAND)
                    .body [[
                        ctl.Panel(wx.BoxSizer(wx.VERTICAL), label="Panel1")
                            .body [[
                                ctl.StaticText(label="StaticText1"),
                            ]],
                        ctl.ScrollablePanel(wx.BoxSizer(wx.VERTICAL), label="Panel2")
                            .body [[
                                ctl.StaticText(label="StaticText1"),
                            ]],
                        ctl.Panel(wx.BoxSizer(wx.VERTICAL), label="Panel3")
                            .body [[
                                ctl.StaticText(label="StaticText1"),
                            ]],
                    ]],
                ctl.Notebook()
                    .sizer(proportion=1, flag=wx.EXPAND),
                ctl.CollapsiblePanel(sizer=wx.BoxSizer(), label="CollapsiblePanel")
                    .sizer(proportion=1, flag=wx.EXPAND)
                    .body [[
                        ctl.StaticText(label="StaticText"),
                    ]],
                ctl.CollapsiblePanel(sizer=wx.BoxSizer(), label="CollapsiblePanel")
                    .sizer(proportion=1, flag=wx.EXPAND),
                ctl.ScrollablePanel(sizer=wx.BoxSizer())
                    .sizer(proportion=1, flag=wx.EXPAND)
                    .body [[
                        ctl.StaticText(label="StaticText"),
                    ]],
                ctl.ScrollablePanel(sizer=wx.BoxSizer())
                    .sizer(proportion=1, flag=wx.EXPAND),
                ctl.StaticBox(sizer=wx.BoxSizer())
                    .sizer(proportion=1, flag=wx.EXPAND)
                    .body [[
                        ctl.StaticText(label="StaticText"),
                    ]],
                ctl.StaticBox(sizer=wx.BoxSizer())
                    .sizer(proportion=1, flag=wx.EXPAND),
            ]]
        )

class TestClass(unittest.TestCase):
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
