# Library Imports
import wx
from typing import TypeVar, Generic, Callable, Any, Union
import itertools
import threading

# Internal Imports


EVT_MUTATION = wx.NewEventType()

IDGenerator = itertools.count()

T = TypeVar("T")
class MutationEvent(Generic[T], wx.PyCommandEvent):
    def __init__(self, id: int, oldValue: T, newValue: T):
        super().__init__(EVT_MUTATION, id)
        self.__oldValue = oldValue
        self.__newValue = newValue

    @property
    def oldValue(self) -> T:
        return self.__oldValue

    @property
    def newValue(self) -> T:
        return self.__newValue

T = TypeVar("T")
SYNC_GETTER_TYPE = Union[Callable[[], T], tuple[object, str]]

T = TypeVar("T")
SYNC_SETTER_TYPE = Union[Callable[[T], None], tuple[object, str]]

T = TypeVar("T")
class Mutable(Generic[T]):
    def __init__(self, val: T):
        self.rawValue = val
        self.evtId = next(IDGenerator)
        self.evtBinder = wx.PyEventBinder(EVT_MUTATION, 1)
        self.evtHandler = wx.EvtHandler()

    def addListener(self, func: Callable[[MutationEvent], None]):
        self.evtBinder.Bind(self.evtHandler, self.evtId, wx.ID_ANY, func)
        evt = MutationEvent(self.evtId, self.rawValue, self.rawValue)
        self.evtHandler.ProcessEvent(evt)

    @property
    def value(self) -> T:
        return self.rawValue

    @value.setter
    def value(self, val: T):
        evt = MutationEvent(self.evtId, self.rawValue, val)
        self.rawValue = val
        self.evtHandler.ProcessEvent(evt)

    def syncFrom(self, getter: SYNC_GETTER_TYPE[T]) -> Callable[[wx.Event], None]:
        def sync_getter():
            if isinstance(getter, tuple):
                value = getattr(getter[0], getter[1])
            else:
                value = getter()
            if self.value != value:
                self.value = value
        def listener(evt: wx.Event):
            sync_getter()
            evt.Skip()
        sync_getter()
        return listener

    def syncTo(self, setter: SYNC_SETTER_TYPE[T]):
        def listener(evt: MutationEvent):
            if isinstance(setter, tuple):
                setattr(setter[0], setter[1], evt.newValue)
            else:
                setter(evt.newValue)
            evt.Skip()
        self.addListener(listener)

    def sync(self, getter: SYNC_GETTER_TYPE[T], setter: SYNC_SETTER_TYPE[T]) -> Callable[[wx.Event], None]:
        self.syncTo(setter)
        return self.syncFrom(getter)

T = TypeVar("T")
MutableValue = Union[Mutable[T], T]

T = TypeVar("T")
def ismutable(val: MutableValue[T]) -> bool:
    return isinstance(val, Mutable)

T = TypeVar("T")
def valueof(val: MutableValue[T]) -> T:
    return val.value if ismutable(val) else val
