# Library Imports
import wx
import wx.svg as svg
import re
import abc
from typing import Union

# Internal Imports


ART_PREFIX = "UI_"

def ArtID(name: str, color: Union[wx.Colour, tuple, None]=None):
    if not isinstance(color, tuple):
        color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT).Get() if color is None else color.Get()
    assert isinstance(color, tuple)
    colortuple = color[:3]
    return f"{ART_PREFIX}{name}_#%02X%02X%02X" % colortuple

class SVGArtProvider(wx.ArtProvider):
    def CreateBitmap(self, artid: str, client: str, size: wx.Size):
        if artid.startswith(ART_PREFIX):
            fmtgrp = re.search(r'^([\w-]+)_(#[0-9a-fA-F]{6})', artid.removeprefix(ART_PREFIX))
            assert fmtgrp is not None
            name, colorstr = fmtgrp.groups()
            color = wx.Colour()
            color.Set(colorstr)
            img: wx.Image = svg.SVGimage.CreateFromFile(self.getIconPath(name)).ConvertToScaledBitmap(size.Scale(2, 2)).ConvertToImage()
            img.Replace(0, 0, 0, *color.Get(includeAlpha=False))
            return img.ConvertToBitmap()
        else:
            return super().CreateBitmap(artid, client, size)

    @abc.abstractmethod
    def getIconPath(self, name: str) -> str:
        pass
