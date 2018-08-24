"""
PureFunction represents a pure function.
PureFunction is also a functor that can map function f on its function self
to generate a new function. Thus, a series of functions can be composited by 
generating new PureFunction instance and finally get a complex function.
"""

from doufo.control import Monad, Functor
from functools import partial, wraps
import functools
import inspect
from typing import Callable, Union, Generic, cast, Any, TypeVar
from abc import ABCMeta, abstractmethod

__all__ = ['Function', 'func', 'identity', 'flip']

from typing import TypeVar
from numba import jit

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


class Function(Callable[[A], B], Monad[Callable[[A], B]]):
    def __init__(self, f, *, nargs=None, nouts=None):
        self.f = f
        self._nargs = nargs or guess_nargs(f)
        self._nouts = nouts

    def __call__(self, *args, **kwargs) -> Union['Function', B]:
        # HACK force call with syntax f()
        if len(args) == 0 and len(kwargs) == 0:
            return self.f()
        if nargs_left(self.nargs, args) == 0:
            return self.f(*args, **kwargs)
        return Function(partial(self.unbox(), *args, **kwargs), nargs=nargs_left(self.nargs, args))

    def bind(self, f: 'Function') -> 'Function':
        return self.fmap(f)

    def fmap(self, f: 'Function') -> 'Function':
        if not isinstance(f, Function):
            f = Function(f)
        return Function(lambda *args, **kwargs: f(self.__call__(*args, **kwargs)), nargs=f.nargs)

    def __matmul__(self, f: 'Function') -> 'Function':
        def foo(*args):
            mid = f(*args[:f.nargs])
            return self(mid, *args[f.nargs:])

        return Function(foo, nargs=self.nargs - f.nargs + 1)

    def unbox(self) -> Callable[..., B]:
        return self.f

    @property
    def nargs(self):
        return self._nargs

    @property
    def nouts(self):
        return self._nouts


def nargs_left(nargs, args):
    if nargs is None:
        return None
    return nargs - len(args)


def guess_nargs(f):
    if isinstance(f, Function) and f.nargs is not None:
        return f.nargs
    spec = inspect.getfullargspec(f)
    if spec.varargs is not None:
        return None
    if spec.defaults is None:
        nb_defaults = 0
    else:
        nb_defaults = len(spec.defaults)
    return len(spec.args) - nb_defaults


def func(nargs=None):
    """
    decorate normal function to PureFunction with parameter number.

    """

    def inner(f: Callable) -> Function:
        return cast(Function, wraps(f)(Function(f, nargs=nargs)))

    return inner


identity = Function[A, A](lambda x: x)


@func()
def flip(f: Callable[[A], B]) -> Function[B, A]:
    """
    flip order of first two arguments to function.
    """

    @wraps(f)
    def inner(*args, **kwargs):
        return f(args[1], args[0], *args[2:], **kwargs)

    return inner
