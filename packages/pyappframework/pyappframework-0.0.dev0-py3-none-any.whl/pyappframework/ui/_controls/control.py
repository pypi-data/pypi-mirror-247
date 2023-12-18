# Library Imports
import wx

# Internal Imports
from .. import attribute as attr
from ..view import PrimitiveView

class Control(PrimitiveView):
    def __init__(self):
        super().__init__()
        self.sizer = attr.Attribute(self, attr.SizerChildAttributeHandler(), None, 1)
        self.eventHandler = attr.Attribute(self, attr.EventHandlerAttributeHandler[wx.Window, wx.Window, wx.Window](), None)
        self.export = attr.Attribute(self, attr.ExportAttributeHandler[wx.Window, wx.Window, wx.Window](), None, 1)
        self.visible = attr.Attribute(self, attr.VisibilityAttributeHandler(), None, 1)
        self.tooltip = attr.Attribute(self, attr.ToolTipAttributeHandler(), None, 1)
        self.rawModifier = attr.Attribute(self, attr.RawModifierAttributeHandler(), None, 1)
        self.font = attr.Attribute(self, attr.FontAttributeHandler(), None, 1)
