from .function import Function, guess_nargs
from functools import wraps
from multipledispatch import Dispatcher
import functools

__all__ = ['singledispatch', 'SingleDispatchFunction', 'multidispatch', 'MultiDispatchFunction']


def singledispatch(*, nargs=None):
    """
    decorate of both functools.singledispatch and func
    """

    def wrapper(f):
        return wraps(f)(SingleDispatchFunction(f, nargs=nargs))

    return wrapper


class SingleDispatchFunction(Function):
    def __init__(self, f, nargs=None):
        if nargs is None:
            nargs = guess_nargs(f)
        super().__init__(functools.singledispatch(f), nargs=nargs)
        self.registered = {}

    def register(self, *args, **kwargs):
        result = self.f.register(*args, **kwargs)
        if len(args) > 0:
            self.registered[args[0]] = result
        return result


def multidispatch(*, nargs=None):
    def wrapper(f):
        return wraps(f)(MultiDispatchFunction(f, nargs=nargs))

    return wrapper


class MultiDispatchFunction(Function):
    def __init__(self, f, *, nargs=None):
        nargs = nargs or guess_nargs(f)
        super().__init__(Dispatcher(f.__name__), nargs=nargs)
        if self.nargs is None:
            raise TypeError("Explict nargs is required for multidispatch.")
        self.register(*([object] * self.nargs))(f)

    def register(self, *types):
        return self.f.register(*types)
