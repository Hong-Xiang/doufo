from doufo import Monad
from functools import partial, wraps
import inspect
from typing import Callable, Union, Generic, cast, Any

__all__ = ['PureFunction', 'func', 'identity', 'flip']

from typing import TypeVar


A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


class PureFunction(Callable[[A], B], Monad[Callable[[A], B]]):
    def __init__(self, f, *, nargs=None):
        self.f = f
        if nargs is None:
            nargs = len(inspect.getfullargspec(f).args)
        self.nargs = nargs

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

    # def apply(self, x):
        # return PureFunction(partial(self.__call__, x))


def func(f: Callable) -> PureFunction:
    return cast(PureFunction, wraps(f)(PureFunction(f)))


identity: PureFunction[A, A] = func(lambda x: x)


@func
def flip(f: Callable[[A], B]) -> PureFunction[B, A]:
    @wraps(f)
    def inner(*args, **kwargs):
        return f(args[1], args[0], *args[2:], **kwargs)
    return inner
