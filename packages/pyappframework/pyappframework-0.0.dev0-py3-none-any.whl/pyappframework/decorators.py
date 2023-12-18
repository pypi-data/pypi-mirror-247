# Library Imports
from typing import Callable, TypeVar
from typing_extensions import ParamSpec, Concatenate
import wx

T = TypeVar("T")
P = ParamSpec("P")
def chainable(func: Callable[Concatenate[T, P], None]) -> Callable[Concatenate[T, P], T]:
    def func_wrapper(self: T, *args: P.args, **kw: P.kwargs) -> T:
        func(self, *args, **kw)
        return self
    return func_wrapper

T = TypeVar("T")
E = TypeVar("E", bound=wx.Event)
def event_handler(func: Callable[[T, E], None]) -> Callable[[T, E], None]:
    def func_wrapper(self: T, evt: E) -> None:
        func(self, evt)
        evt.Skip()
    return func_wrapper
