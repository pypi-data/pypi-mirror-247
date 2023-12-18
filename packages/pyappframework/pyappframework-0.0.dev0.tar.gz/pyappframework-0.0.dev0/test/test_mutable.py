# Library Imports
import unittest
import wx

# Internal Imports
import pyappframework as pyaf

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()
        self.mutable = pyaf.Mutable[int](0)
        self.passed = False

    def tearDown(self):
        self.app.Destroy()

    def runTest(self):
        self.mutable.addListener(self.mutationListener)
        self.mutable.value += 1
        self.assertTrue(self.passed)

    def mutationListener(self, evt: pyaf.MutationEvent):
        if evt.oldValue == 0 and evt.newValue == 1:
            self.passed = True
