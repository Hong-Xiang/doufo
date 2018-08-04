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
    return len(inspect.getfullargspec(f).args)

class SingleDispatchFunction(PureFunction):
    def __init__(self, f):
        super().__init__(functools.singledispatch(f), nargs=guess_nargs(f))

    def register(self, *args, **kwargs):
        return self.f.register(*args, **kwargs)


def singledispatch(f):
    return SingleDispatchFunction(f)

def func(f: Callable) -> PureFunction:
    return cast(PureFunction, wraps(f)(PureFunction(f)))


identity: PureFunction[A, A] = func(lambda x: x)


@func
def flip(f: Callable[[A], B]) -> PureFunction[B, A]:
    @wraps(f)
    def inner(*args, **kwargs):
        return f(args[1], args[0], *args[2:], **kwargs)
    return inner
