# Library Imports
import unittest
import wx
from matplotlib.figure import Figure
import numpy as np

# Internal Imports
from pyappframework import ui
from pyappframework.ui import controls as ctl
from pyappframework.ui._controls import plot as plot

class TestWindow(ui.Window):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.SetTitle("TestWindow")

    def body(self) -> ctl.Panel:
        figure = Figure()
        axes = figure.add_subplot()
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        axes.plot(t, s)
        return (
            ctl.Panel(wx.BoxSizer(wx.VERTICAL))
            .body [[
                plot.Plot(wx.ID_ANY, figure)
                    .sizer(proportion=1, flag=wx.EXPAND)
            ]]
        )

class PlotTest(unittest.TestCase):
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
