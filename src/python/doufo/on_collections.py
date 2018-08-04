from typing import Iterable, TypeVar, List, Union, TYPE_CHECKING, Tuple, Optional, Sequence, Any
from doufo import func, singledispatch
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
def _(xs: Iterable[T], n: int) -> Iterable[T]:
    return xs[:n]


@func
def head(xs: Iterable[T]):
    return head_(xs)


@singledispatch
def head_(xs: Iterable[T]):
    return next(iter(xs))

@singledispatch
def tail(xs: Iterable[T]):
    pass

@tail.register(Sequence[T])
def _(xs:Sequence[T]) -> Sequence[T]:
    return x[1:]

@singledispatch
def concat(xss: Sequence[Iterable[T]], acc: Optional[Iterable[T]]=None) -> Iterable[T]:
    if len(xss) == 0:
        return List([])
    if isinstance(xss[0], list):
        return functools.reduce(operator.add, xss, acc)
    return functools.reduce(operator.methodcaller('extends'), xss, acc)


@func
def fzip(*xss: Tuple[Iterable]) -> Iterable[Tuple]:
    return zip_(xss)


@singledispatch
def zip_(xss):
    return zip(*xss)


@singledispatch
def flatten(x: Iterable[T]) -> Iterable[T]:
    return x


@flatten.register(tuple)
def _(xs: Tuple[Union[T, Any]]) -> Tuple[T]:
    return tuple([flatten(x) for x in xs])
