from .control import Monad
from functools import partial

from typing import TypeVar, Callable

T = TypeVar('T')
B = TypeVar('B')


class Maybe(Monad[T]):
    def __init__(self, data):
        self.data = data

    def __eq__(self, m):
        return isinstance(m, Maybe) and m.unbox() == self.unbox()

    def unbox(self) -> T:
        return self.data

    def fmap(self, f: Callable[[T], B]) -> 'Maybe[B]':
        return Maybe(None) if self.unbox() is None else Maybe(f(self.unbox()))

    def apply(self, v):
        return self.fmap(lambda f: partial(f, v))

    def bind(self, f: Callable[[T], 'Maybe[B]']) -> 'Maybe[B]':
        return self.fmap(lambda x: f(x).unbox())
