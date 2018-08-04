from functools import singledispatch
from typing import Iterable, TypeVar, List, Union, TYPE_CHECKING, Tuple, Optional, Sequence, Any
from .function import func
import collections.abc
import itertools

__all__ = ['take', 'head', 'concat', 'fzip']

T = TypeVar('T')


@func
def take(n: int, xs: Iterable[T]) -> Iterable[T]:
    return take_(xs, n)


@singledispatch
def take_(xs: Iterable[T], n: int) -> Iterable[T]:
    raise TypeError(f"Invalid type of xs: {type(xs)}.")


@take_.register(collections.abc.Sequence)
def take_(xs: Iterable[T], n: int) -> Iterable[T]:
    return xs[:n]


@func
def head(xs: Iterable[T]):
    return head_(xs)


@singledispatch
def head_(xs: Iterable[T]):
    return next(iter(xs))


@func
@singledispatch
def concat(xss: Sequence[Iterable[T]], acc: Optional[Iterable[T]]=None) -> Iterable[T]:
    return functools.reduce(operator.methodcaller('extends'), xss, acc)


@concat.register(list)
def _(xss: List[T], acc: List[T]=None) -> List[T]:
    return functools.reduce(operator.add, xss, acc)


@func
def fzip(*xss: Tuple[Iterable]) -> Iterable[Tuple]:
    return zip_(xss)


@singledispatch
def zip_(xss):
    return zip(*xss)


@func
@singledispatch
def flatten(x: Iterable[T]) -> Iterable[T]:
    return x


@flatten.register(tuple)
def _(xs: Tuple[Union[T, Any]]) -> Tuple[T]:
    return tuple([flatten(x) for x in xs])
