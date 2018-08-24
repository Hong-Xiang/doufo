from .function import WrappedFunction, guess_nargs
from functools import wraps
from multipledispatch import Dispatcher
import functools

__all__ = ['singledispatch', 'SingleDispatchFunction', 'multidispatch', 'MultiDispatchFunction']


def singledispatch(*, nargs=None, nouts=None):
    """
    decorate of both functools.singledispatch and func
    """

    def wrapper(f):
        return wraps(f)(SingleDispatchFunction(f, nargs=nargs, nouts=None))

    return wrapper


class SingleDispatchFunction(WrappedFunction):
    def __init__(self, f, nargs=None, nouts=None):
        super().__init__(functools.singledispatch(f), nargs=nargs if nargs is not None else guess_nargs(f), nouts=nouts)
        self.registered = {}

    def register(self, *args, **kwargs):
        result = self.f.register(*args, **kwargs)
        if len(args) > 0:
            self.registered[args[0]] = result
        return result


def multidispatch(*, nargs=None, nouts=None):
    def wrapper(f):
        return wraps(f)(MultiDispatchFunction(f, nargs=nargs, nouts=nouts))

    return wrapper


class MultiDispatchFunction(WrappedFunction):
    def __init__(self, f, *, nargs=None, nouts=None):
        super().__init__(Dispatcher(f.__name__), nargs=nargs if nargs is not None else guess_nargs(f), nouts=nouts)
        if self.nargs is None:
            raise TypeError("Explict nargs is required for multidispatch.")
        self.register(*([object] * self.nargs))(f)

    def register(self, *types):
        return self.f.register(*types)
