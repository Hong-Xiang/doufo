"""
This file provide the common operations on the data.
All the operations are warpped as a PureFunction and single dispatched for 
specfic data type.
Example:
    head: get the data from the start.
...
"""
from typing import Iterable, TypeVar, List, Union, TYPE_CHECKING, Tuple, Optional, Sequence, Any
from doufo import func, singledispatch
import collections.abc
import itertools
import functools
import operator


__all__ = ['take', 'head', 'concat', 'fzip', 'tail', 'flatten', 'concat', 'all_isinstance', 'fmap']

T = TypeVar('T')


@func()
def take(n: int, xs: Iterable[T]) -> Iterable[T]:
    return take_(xs, n)


@singledispatch()
def take_(xs: Iterable[T], n: int) -> Iterable[T]:
    raise TypeError(f"Invalid type of xs: {type(xs)}.")


@take_.register(collections.abc.Sequence)
def _(xs: Iterable[T], n: int) -> Iterable[T]:
    return xs[:n]


@func()
def head(xs: Iterable[T]):
    return head_(xs)


@singledispatch()
def head_(xs: Iterable[T]):
    return next(iter(xs))


@singledispatch()
def tail(xs: Iterable[T]):
    raise NotImplementedError()


@tail.register(collections.abc.Sequence)
def _(xs: Sequence[T]) -> Sequence[T]:
    return xs[1:]


@func()
def concat(xss: Sequence[Iterable[T]], acc: Optional[Iterable[T]]) -> Iterable[T]:
    if len(xss) == 0:
        return List([])
    if isinstance(xss[0], list):
        return concat_kernel(xss, operator.add, acc)
    if isinstance(xss[0], tuple):
        return tuple(concat_kernel([list(x) for x in xss], operator.add, acc))
    if acc is None:
        return functools.reduce(lambda xs, t: xs.extend(t), xss)
    else:
        return functools.reduce(lambda xs, t: xs.extend(t), xss, acc)


def concat_kernel(xss, op, acc):
    if acc is None:
        return functools.reduce(op, xss)
    else:
        return functools.reduce(op, xss, acc)


@func()
def fzip(*xss: Tuple[Iterable]) -> Iterable[Tuple]:
    return zip_(xss)


@singledispatch()
def zip_(xss):
    return zip(*xss)


@singledispatch()
def flatten(x: Iterable[T]) -> Iterable[T]:
    return x


@flatten.register(list)
def _(xs: Tuple[Union[T, Any]]) -> Tuple[T]:
    return concat([flatten(x) if isinstance(x, list) else [x]
                   for x in xs], None)


@flatten.register(tuple)
def _(xs: Tuple[Union[T, Any]]) -> Tuple[T]:
    return tuple(concat([flatten(x) if isinstance(x, tuple) else (x,)
                         for x in xs], None))


@singledispatch(nargs=2, nouts=1)
def all_isinstance(xs, type_):
    return all(map(lambda o: isinstance(o, type_), xs))


@singledispatch(nargs=2, nouts=1)
def fmap(xs, f):
    return xs.fmap(f)


@fmap.register(list)
def fmap(xs, f):
    return [f(x) for x in xs]
