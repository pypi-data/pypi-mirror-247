# Library Imports
import wx
import abc
from typing import Callable, Optional, Generic, Any, TypeVar, Union

# Internal Imports
from ..decorators import event_handler
from ..mutable import Mutable, MutationEvent

# R: Generic type for root
# P: Generic type for parent
# T: Generic type for Target
# V: Generic type for Value
R, P, T = (TypeVar("R"), TypeVar("P"), TypeVar("T"))
class AttributeContainer(Generic[R, P, T]):
    def __init__(self):
        self.__attrib_delegates = []

    def addAttribDelegate(self, func: Callable[[R, P, T], None]):
        self.__attrib_delegates.append(func)

    def runAttribDelegates(self, root: R, parent: P, target: T):
        for delegate in self.__attrib_delegates:
            delegate(root, parent, target)

R, P, T = (TypeVar("R"), TypeVar("P"), TypeVar("T"))
class AttributeHandler(Generic[R, P, T]):
    @abc.abstractmethod
    def _handle_value(self, obj: AttributeContainer[R, P, T], *args, **kw) -> Any:
        pass

R, P, T = (TypeVar("R"), TypeVar("P"), TypeVar("T"))
class Attribute(Generic[R, P, T]):
    def __init__(self, obj: AttributeContainer[R, P, T], handler: Optional[AttributeHandler[R, P, T]] = None, default = None, count: int = -1):
        self.obj = obj
        self.handler = handler
        self.value = default
        self.count = count

    def checkCount(self):
        if self.count >= 0:
            assert self.count > 0
            self.count -= 1

    def __call__(self, *args, **kw) -> Any:
        self.checkCount()
        if self.handler is not None:
            self.value = self.handler._handle_value(self.obj, *args, **kw)
        else:
            self.value = (args, kw)
        return self.obj

    __getitem__ = __call__

R, P, T = (TypeVar("R"), TypeVar("P"), TypeVar("T"))
class ArgumentAttribute(Generic[R, P, T], Attribute[R, P, T]):
    def __init__(self, obj: AttributeContainer[R, P, T]):
        super().__init__(obj, None, None, 1)
        self.value = ((), {})
    
    def __call__(self, *args, **kw) -> Any:
        self.checkCount()
        self.value = (args, kw)
        return self.obj
    
    __getitem__ = __call__

    def getArgs(self) -> tuple[tuple, dict]:
        return self.value

R, P, T, V = (TypeVar("R"), TypeVar("P"), TypeVar("T"), TypeVar("V"))
class TypedAttribute(Generic[R, P, T, V], Attribute[R, P, T]):
    def __init__(self, obj: AttributeContainer[R, P, T]):
        super().__init__(obj, None, None, 1)

    def __call__(self, val: V, /) -> Any:
        self.checkCount()
        self.value = val
        return self.obj

    __getitem__ = __call__

    def getTypedValue(self) -> Optional[V]:
        return self.value

class SizerChildAttributeHandler(AttributeHandler[wx.Window, wx.Window, wx.Window]):
    def _handle_value(self, obj: AttributeContainer[wx.Window, wx.Window, wx.Window], *args, **kw):
        obj.addAttribDelegate(self._delegate(args, kw))

    def _delegate(self, args, kw):
        def func(root: wx.Window, parent: wx.Window, target: wx.Window):
            parent_sizer = target.GetParent().GetSizer()
            if parent_sizer is not None:
                parent_sizer.Add(target, *args, **kw)
        return func

class FontAttributeHandler(AttributeHandler[wx.Window, wx.Window, wx.Window]):
    def _handle_value(self, obj: AttributeContainer[wx.Window, wx.Window, wx.Window], font: Union[wx.Font, wx.FontInfo]):
        obj.addAttribDelegate(self._delegate(font))

    def _delegate(self, font: Union[wx.Font, wx.FontInfo]):
        if isinstance(font, wx.FontInfo):
            font = wx.Font(font)
        def func(root: wx.Window, parent: wx.Window, target: wx.Window):
            target.SetFont(font)
        return func

R, P, T = (TypeVar("R"), TypeVar("P"), TypeVar("T"))
class EventHandlerAttributeHandler(AttributeHandler[R, P, T]):
    def _handle_value(self, obj: AttributeContainer[R, P, T], evt: wx.Event, func: Callable[[wx.Event], None]):
        obj.addAttribDelegate(self._delegate(evt, func))

    def _delegate(self, evt: wx.Event, handler: Callable[[wx.Event], None]):
        def func(root, parent, target):
            root.Bind(evt, handler, target)
        return func

R, P, T = (TypeVar("R"), TypeVar("P"), TypeVar("T"))
class ExportAttributeHandler(Generic[R, P, T], AttributeHandler[R, P, T]):
    def _handle_value(self, obj: AttributeContainer[R, P, T], exportid: str):
        obj.addAttribDelegate(self._delegate(exportid))

    def _delegate(self, exportid: str):
        def func(root, parent, target):
            setattr(root, exportid, target)
        return func

class ToolTipAttributeHandler(AttributeHandler[wx.Window, wx.Window, wx.Window]):
    def _handle_value(self, obj: AttributeContainer[wx.Window, wx.Window, wx.Window], tto: Union[wx.ToolTip, str]):
        obj.addAttribDelegate(self._delegate(tto))

    def _delegate(self, tto: Union[wx.ToolTip, str]):
        def func(root: wx.Window, parent: wx.Window, target: wx.Window):
            target.SetToolTip(tto)
        return func

T = TypeVar("T", bound=wx.Window)
class RawModifierAttributeHandler(AttributeHandler[wx.Window, wx.Window, wx.Window]):
    def _handle_value(self, obj: AttributeContainer[wx.Window, wx.Window, wx.Window], func: Callable[[T], None]):
        obj.addAttribDelegate(self._delegate(func))

    def _delegate(self, modifier: Callable[[T], None]):
        def func(root: wx.Window, parent: wx.Window, target: wx.Window):
            modifier(target)  # type: ignore
        return func

C = TypeVar("C")
CONTENTS_LIST_TYPE = list[C]

C = TypeVar("C")
CONTENTS_LIST_INPUT_TYPE = list[Union[C, CONTENTS_LIST_TYPE[C]]]

R, P, T, V = (TypeVar("R"), TypeVar("P"), TypeVar("T"), TypeVar("V"))
class BodyAttribute(Generic[R, P, T, V], Attribute[R, P, T]):
    def __init__(self, obj: AttributeContainer[R, P, T]):
        super().__init__(obj, None, [], 1)

    def __call__(self, l: CONTENTS_LIST_INPUT_TYPE[V], /) -> Any:
        self.checkCount()
        body = []
        for litem in l:
            if isinstance(litem, list):
                body.extend(litem)
            else:
                body.append(litem)
        self.value: CONTENTS_LIST_TYPE[V] = body
        return self.obj

    __getitem__ = __call__

    def getBody(self) -> CONTENTS_LIST_TYPE[V]:
        return self.value

class VisibilityAttributeHandler(AttributeHandler[wx.Window, wx.Window, wx.Window]):
    def __init__(self):
        super().__init__()
        self.__target = None

    def _handle_value(self, obj: AttributeContainer[wx.Window, wx.Window, wx.Window], vm: Mutable[bool], /):
        obj.addAttribDelegate(self._delegate(obj, vm))

    def _delegate(self, obj: AttributeContainer[wx.Window, wx.Window, wx.Window], vm: Mutable[bool]):
        def func(root: wx.Window, parent: wx.Window, target: wx.Window):
            self.__target = target
            vm.addListener(self._onValueChange)
            target.Show(vm.value)
        return func

    @event_handler
    def _onValueChange(self, evt: MutationEvent):
        assert self.__target is not None
        self.__target.Show(evt.newValue)
        self.__target.GetParent().Layout()
