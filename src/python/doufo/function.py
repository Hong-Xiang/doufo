from doufo import Monad
from functools import partial, wraps
import functools
import inspect
from typing import Callable, Union, Generic, cast, Any

__all__ = ['PureFunction', 'func', 'identity', 'flip', 'singledispatch']

from typing import TypeVar


A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


class PureFunction(Callable[[A], B], Monad[Callable[[A], B]]):
    def __init__(self, f, *, nargs=None):
        self.f = f
        self.nargs = nargs or guess_nargs(f)

    def __call__(self, *args, **kwargs) -> Union['PureFunction', B]:
        if len(args) < self.nargs:
            return PureFunction(partial(self.f, *args, **kwargs))
        return self.f(*args, **kwargs)

    def bind(self, f: 'PureFunction') -> 'PureFunction':
        return self.fmap(f)

    def fmap(self, f: 'PureFunction') -> 'PureFunction':
        return PureFunction(lambda *args, **kwargs: f(self.__call__(*args, **kwargs)))

    def __matmul__(self, f: 'PureFunction') -> 'PureFunction':
        def foo(*args):
            mid = f(*args[:f.nargs])
            return self(mid, *args[f.nargs:])
        return PureFunction(foo, nargs=self.nargs - f.nargs + 1)

    def unbox(self) -> Callable[..., B]:
        return self.f


def guess_nargs(f):
    spec = inspect.getfullargspec(f)
    if spec.defaults is None:
        nb_defaults = 0
    else:
        nb_defaults = len(spec.defaults)
    return len(spec.args) - nb_defaults


class SingleDispatchFunction(PureFunction):
    def __init__(self, f):
        super().__init__(functools.singledispatch(f), nargs=guess_nargs(f))
        self.registed = {}

    def register(self, *args, **kwargs):
        result = self.f.register(*args, **kwargs)
        if len(args) > 0:
            self.registed[args[0]] = result
        return result


def singledispatch(f):
    """
    decorate of both functools.singledispatch and func
    """
    return SingleDispatchFunction(f)


def func(f: Callable) -> PureFunction:
    """
    decorate normal function to PureFunction, for currying, @composite, fmap, etc.
    """
    return cast(PureFunction, wraps(f)(PureFunction(f)))


identity: PureFunction[A, A] = func(lambda x: x)


@func
def flip(f: Callable[[A], B]) -> PureFunction[B, A]:
    """
    flip order of first two arguments to function.
    """
    @wraps(f)
    def inner(*args, **kwargs):
        return f(args[1], args[0], *args[2:], **kwargs)
    return inner
