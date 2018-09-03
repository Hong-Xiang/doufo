"""
Function is a functor that can map function f on its function self
to generate a new function. Thus, a series of functions can be composited by 
generating new PureFunction instance and finally get a complex function.
"""

import inspect
from abc import abstractmethod
from functools import partial, wraps
from typing import Callable, Optional
from multipledispatch import Dispatcher
import functools
from doufo.control import Monad
from typing import TypeVar
import re

__all__ = ['Function', 'WrappedFunction', 'func', 'identity', 'flip', 'singledispatch', 'SingleDispatchFunction',
           'multidispatch', 'MultiDispatchFunction', 'tagfunc']

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
T = TypeVar('T')


class Function(Callable, Monad[Callable]):
    def __call__(self, *args, **kwargs):
        return self.unbox()(*args, **kwargs)

    def bind(self, f: 'Function') -> 'Function':
        return f.fmap(self)

    @abstractmethod
    def fmap(self, f: Callable):
        pass

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

    @property
    @abstractmethod
    def ndefs(self) -> Optional[int]:
        pass


def _nargs(f) -> Optional[int]:
    if isinstance(f, Function):
        return f.nargs
    spec = inspect.getfullargspec(f)
    if spec.varargs is not None:
        return None
    return len(spec.args)


def _ndefs(f):
    if isinstance(f, Function):
        return f.ndefs
    spec = inspect.getfullargspec(f)
    if spec.defaults is None:
        return 0
    return len(spec.defaults)


def _nouts(f):
    if isinstance(f, Function):
        return f.nouts
    return None


def get_nargs(f: Callable, hint: Optional[int]) -> Optional[int]:
    if hint is not None:
        return hint
    else:
        return _nargs(f)


def get_ndefs(f: Callable, hint: Optional[int]) -> Optional[int]:
    if hint is not None:
        return hint
    else:
        return _ndefs(f)


p_few = re.compile(r"[\w()]+ missing (\d+) required positional arguments?: [\w,']+")
p_many = re.compile(r"[\w()]+ takes (\d+) positional arguments?: but (\d+) were given")


class WrappedFunction(Function):
    def __init__(self, f, *, nargs=None, nouts=None, ndefs=None):
        self.f = f
        self._nargs = get_nargs(f, nargs)
        self._nouts = nouts
        self._ndefs = get_ndefs(f, ndefs) or 0

    def __matmul__(self, f: 'Function') -> 'Function':
        return self.fmap(f)

    def __call__(self, *args, **kwargs):
        try:
            return self.unbox()(*args, **kwargs)
        except TypeError as e:
            if p_few.match(str(e)):
                if self.is_expand_needed(args):
                    return self.unbox()(*args[0], **kwargs)
                return WrappedFunction(partial(self.unbox(), *args, **kwargs),
                                       nargs=self.left_args(args),
                                       nouts=self.nouts,
                                       ndefs=self.left_defs(args))
            elif p_many.match(str(e)):
                result = self.unbox()(*args[:self.nargs], **kwargs)
                if self.nouts is not None and self.nouts > 1:
                    return (*result, *args[self.nargs:])
                return (result, *args[self.nargs:])
            else:
                raise e

    def fmap(self, f: 'WrappedFunction') -> 'WrappedFunction':
        if not isinstance(f, WrappedFunction):
            f = WrappedFunction(f)
        return WrappedFunction(lambda *args, **kwargs: self(f(*args, **kwargs)), nargs=f.nargs, nouts=self.nouts)

    def is_expand_needed(self, args):
        if len(args) == 1 and isinstance(args[0], tuple):
            if self.nargs is None:
                return False
            if len(args[0]) + self.ndefs >= self.nargs:
                return True
        return False

    def left_args(self, args):
        if self.nargs is None:
            return None
        return self.nargs - len(args)

    def left_defs(self, args):
        if self.nargs is None:
            return self.ndefs
        if len(args) > self.nargs - self.ndefs:
            return self.ndefs - len(args) + self.nargs
        else:
            return self.ndefs

    def unbox(self):
        return self.f

    @property
    def nargs(self):
        return self._nargs

    @property
    def nouts(self):
        return self._nouts

    @property
    def ndefs(self):
        return self._ndefs


def nargs_left(nargs, ndefs, args) -> Optional[int]:
    if nargs is None:
        return None
    if ndefs is None:
        ndefs = 0
    return nargs - len(args)


def func(nargs: Optional[int] = None, nouts: Optional[int] = None, ndefs: Optional[int] = None):
    """
    decorates normal function to Function with (optional) number of arguments and outputs.
    """
    return lambda f: wraps(f)(WrappedFunction(f, nargs=nargs, nouts=nouts, ndefs=ndefs))


@func(nargs=1, nouts=1, ndefs=0)
def nargs(f) -> Optional[int]:
    return _nargs(f)


@func(nargs=1, nouts=1, ndefs=0)
def ndefs(f):
    return _ndefs(f)


@func(nargs=1, nouts=1, ndefs=0)
def nouts(f) -> Optional[int]:
    return _nouts(f)


identity = WrappedFunction(lambda x: x, nargs=1, nouts=1, ndefs=0)


class SingleDispatchFunction(WrappedFunction):
    def __init__(self, f, nargs=None, nouts=None, ndefs=None):
        super().__init__(functools.singledispatch(f),
                         nargs=get_ndefs(f, nargs),
                         nouts=nouts,
                         ndefs=get_ndefs(f, ndefs))
        self.registered = {}

    def register(self, *args, **kwargs):
        result = self.f.register(*args, **kwargs)
        if len(args) > 0:
            self.registered[args[0]] = result
        return result


def singledispatch(*, nargs=None, nouts=None, ndefs=None):
    """
    decorate of both functools.singledispatch and func
    """

    def wrapper(f):
        return wraps(f)(SingleDispatchFunction(f, nargs=nargs, nouts=nouts, ndefs=ndefs))

    return wrapper


class MultiDispatchFunction(WrappedFunction):
    def __init__(self, f, *, nargs=None, nouts=None):
        super().__init__(Dispatcher(f.__name__),
                         nargs=get_nargs(f, nargs),
                         nouts=nouts,
                         ndefs=get_ndefs(f, ndefs))
        if self.nargs is None:
            raise TypeError("Explict nargs is required for multidispatch.")
        self.register(*([object] * self.nargs))(f)

    def register(self, *types):
        def decorator(f):
            self.f.add(types, f)
            return f

        return decorator


def multidispatch(*, nargs=None, nouts=None):
    def wrapper(f):
        return wraps(f)(MultiDispatchFunction(f, nargs=nargs, nouts=nouts))

    return wrapper


@func()
def flip(f: Callable) -> Function:
    """
    flip order of first two arguments to function.
    """
    nargs_, nouts_, ndefs_ = nargs(f), nouts(f), ndefs(f)
    return WrappedFunction(lambda *args, **kwargs: f(args[1], args[0], *args[2:], **kwargs),
                           nargs=nargs_, nouts=nouts_, ndefs=ndefs_)


class FunctionWithTag(Function):
    def __init__(self, default_func, *, nargs=None, nouts=None, ndefs=None):
        self.default_func = default_func
        self._nargs = get_nargs(default_func, nargs)
        self._nouts = nouts
        self._ndefs = get_nargs(default_func, nouts)
        self.methods = {}

    def __getitem__(self, item):
        if item is None and not item in self.methods:
            return self.default_func
        return self.methods[item]

    def register(self, tag):
        def wrapper(f):
            self.methods[tag] = f
            return f

        return wrapper

    def __call__(self, *args, **kwargs):
        return self.default_func(*args, **kwargs)

    @property
    def nargs(self):
        return self._nargs

    @property
    def ndefs(self):
        return self._ndefs

    @property
    def nouts(self):
        return self._nouts

    def fmap(self, f: 'WrappedFunction') -> 'WrappedFunction':
        if not isinstance(f, WrappedFunction):
            f = WrappedFunction(f)
        return WrappedFunction(lambda *args, **kwargs: self(f(*args, **kwargs)), nargs=f.nargs, nouts=self.nouts)

    def unbox(self):
        return self.default_func


def tagfunc(nargs=None, ndefs=None, nouts=None):
    def wrapper(f):
        return wraps(f)(FunctionWithTag(f, nargs=nargs, nouts=nouts, ndefs=ndefs))

    return wrapper
