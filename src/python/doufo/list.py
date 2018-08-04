from typing import Sequence, TypeVar, Any, Union, Callable, Tuple
import typing
from collections import UserList
from .control import Functor

T = TypeVar('T')
B = TypeVar('B')

__all__ = ['List']


class List(UserList, Sequence[T], Functor[T]):
    def __init__(self, data):
        if isinstance(data, List):
            super().__init__(data.unbox())
        else:
            super().__init__(data)

    @classmethod
    def empty(self) -> 'List[Any]':
        return List([])

    def __getitem__(self, x: Union[int, slice]) -> Union[T, 'List[T]']:  # type: ignore
        if isinstance(x, int):
            return self.unbox()[x]
        if isinstance(x, slice):
            return type(self)(self.unbox()[x])
        raise TypeError(
            f"List indices must be integers or slices, not {type(x)}")

    def extend(self, xs: Union['List[T]', typing.List[T]]) -> 'List[T]':  # type: ignore
        return type(self)(self.unbox() + List(xs).unbox())

    def unbox(self) -> typing.List[T]:
        return self.data

    def fmap(self, f: Callable[[T], B]) -> 'List[B]':
        return List([f(x) for x in self.unbox()])

    def zip(self, xs: 'List[B]') -> 'List[Tuple[T, B]]':
        return List([(x, y) for x, y in zip(self, xs)])
