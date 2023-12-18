# Library Imports
from typing import Iterable, Callable, Union, Optional
import wx
import abc
from typing_extensions import Self

# Internal Imports
from ..decorators import chainable
from .attribute import AttributeContainer
from . import attribute as attr

MENUBAR_TYPES = Union[wx.Menu, wx.MenuItem, wx.MenuBar]

class MenuComponent(AttributeContainer[wx.Window, Optional["MenuComponent"], MENUBAR_TYPES]):
    def __init__(self):
        super().__init__()
        self.__wx_instance = None

    def initialize(self, root: wx.MenuBar, parent: Optional["MenuComponent"]) -> MENUBAR_TYPES:
        self.__wx_instance = self._initialize(root, parent)
        self.runAttribDelegates(root, parent, self.__wx_instance)
        return self.__wx_instance

    def setWxInstance(self, instance: MENUBAR_TYPES):
        self.__wx_instance = instance
    
    def getWxInstance(self) -> MENUBAR_TYPES:
        assert self.__wx_instance is not None
        return self.__wx_instance

    @abc.abstractmethod
    def _initialize(self, root: wx.MenuBar, parent: Optional["MenuComponent"]) -> MENUBAR_TYPES:
        pass

class Menu(MenuComponent):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)
        self.body = attr.BodyAttribute(self)

    def _initialize(self, root: wx.MenuBar, parent: Optional[MenuComponent]) -> wx.Menu:
        menu = wx.Menu()
        self.setWxInstance(menu)
        items = self.body.value
        if isinstance(items, list):
            for item in items:
                assert isinstance(item, MenuComponent)
                item.initialize(root, self)
        if parent is None:
            root.Append(menu, *self.__init_args[0], **self.__init_args[1])
        else:
            instance = parent.getWxInstance()
            assert isinstance(instance, wx.Menu)
            instance.AppendSubMenu(menu, *self.__init_args[0], **self.__init_args[1])
        return menu

class MenuItem(MenuComponent):
    def __init__(self, *args, **kw):
        super().__init__()
        self.__init_args = (args, kw)
        self.eventHandler = attr.Attribute(self, attr.EventHandlerAttributeHandler[wx.Window, Optional[MenuComponent], MENUBAR_TYPES]())

    def _initialize(self, root: wx.MenuBar, parent: Optional[MenuComponent]) -> wx.MenuItem:
        assert parent is not None
        instance = parent.getWxInstance()
        assert isinstance(instance, wx.Menu)
        item = instance.Append(*self.__init_args[0], **self.__init_args[1])
        return item

class MenuSeparator(MenuComponent):
    def __init__(self, *args, **kw):
        super().__init__()

    def _initialize(self, root: wx.MenuBar, parent: Optional[MenuComponent]) -> wx.MenuItem:
        assert parent is not None
        instance = parent.getWxInstance()
        assert isinstance(instance, wx.Menu)
        item = instance.AppendSeparator()
        return item
