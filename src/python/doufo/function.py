"""
Function is a functor that can map function f on its function self
to generate a new function. Thus, a series of functions can be composited by 
generating new PureFunction instance and finally get a complex function.
"""

import inspect
from functools import partial, wraps
from typing import Callable, Union, cast, Optional, Generic
from abc import abstractmethod

from doufo.control import Monad

__all__ = ['Function', 'WrappedFunction', 'func', 'identity', 'flip']

from typing import TypeVar

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
T = TypeVar('T')


class Function(Callable, Monad[Callable]):
    def __call__(self, *args, **kwargs):
        # HACK force call with syntax f()
        if len(args) == 0 and len(kwargs) == 0:
            return self.f()
        if nargs_left(self.nargs, args) == 0:
            return self.f(*args, **kwargs)
        return WrappedFunction(partial(self.unbox(), *args, **kwargs), nargs=nargs_left(self.nargs, args))

    def bind(self, f: 'Function') -> 'Function':
        return f.fmap(self)

    def __matmul__(self, f: 'Function') -> 'Function':
        def foo(*args):
            mid = f(*args[:f.nargs])
            return self(mid, *args[f.nargs:])

        return WrappedFunction(foo, nargs=self.nargs - f.nargs + 1)

    @abstractmethod
    def unbox(self) -> Callable:
        pass

    @property
    @abstractmethod
    def nargs(self) -> Optional[int]:
        pass

    @property
    @abstractmethod
    def nouts(self) -> Optional[int]:
        pass


class WrappedFunction(Function):
    def __init__(self, f, *, nargs=None, nouts=None):
        self.f = f
        self._nargs = nargs if nargs is not None else guess_nargs(f)
        self._nouts = nouts

    def fmap(self, f: 'WrappedFunction') -> 'WrappedFunction':
        if not isinstance(f, WrappedFunction):
            f = WrappedFunction(f)
        if f.nouts is None or f.nouts == 1:
            def target(*args, **kwargs):
                return self.__call__(f(*args, **kwargs))
        else:
            def target(*args, **kwargs):
                return self.__call__(*f(*args, **kwargs))
        return WrappedFunction(target, nargs=f.nargs, nouts=self.nouts)

    def unbox(self):
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


def func(nargs: Optional[int] = None, nouts: Optional[int] = None):
    """
    decorates normal function to Function with (optional) number of arguments and outputs.
    """
    return lambda f: wraps(f)(WrappedFunction(f, nargs=nargs, nouts=nouts))


identity = WrappedFunction(lambda x: x, nargs=1, nouts=1)


@func()
def flip(f: Callable) -> Function:
    """
    flip order of first two arguments to function.
    """
    if isinstance(f, Function):
        nargs, nouts = f.nargs, f.nouts
    else:
        nargs, nouts = guess_nargs(f), None
    return WrappedFunction(lambda *args, **kwargs: f(args[1], args[0], *args[2:], **kwargs), nargs=nargs, nouts=nouts)
