from .function import PureFunction, guess_nargs
from functools import wraps
from multipledispatch import Dispatcher

__all__ = ['multidispatch', 'MultiDispatchFunction']

def multidispatch(*, nargs=None):
    def wrapper(f):
        return wraps(f)(MultiDispatchFunction(f, nargs=nargs))
    return wrapper

class MultiDispatchFunction(PureFunction):
    def __init__(self, f, *, nargs=None):
        nargs = nargs or guess_nargs(f)
        super().__init__(Dispatcher(f.__name__), nargs=nargs)
        if self.nargs is None:
            raise TypeError("Explict nargs is required for multidispatch.")
        self.register(*([object]*self.nargs))(f)

    def register(self, *types):
        return self.f.register(*types)




