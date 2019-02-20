from __future__ import annotations
import collections.abc
import typing as T
import abc
import numpy

FUNCTOR_KEYWORD = "__map__"
ITERABLE_KEYWORD = "__is_iterable__"

__all__ = ["pmap"]

A = T.TypeVar("A")
B = T.TypeVar("B")


class Functor(T.Generic[A], abc.ABC):
    @abc.abstractmethod
    def __map__(self, func: T.Callable[[A], B]) -> Functor[B]:
        ...


class PIterable(Functor[A]):
    __is_iterable__ = True

    def __init__(self, source, operation=None):
        self.source = source
        self.operation = operation

    def __map__(self, func: T.Callable[[A], B]) -> Functor[B]:
        return PIterable[B](self, func)

    def __iter__(self):
        if self.operation is None:
            return iter(self.source)
        else:
            return map(self.operation, self.source)


def is_iterable(maybe_iterable):
    if isinstance(maybe_iterable, (range, numpy.ndarray)):
        return True
    elif getattr(maybe_iterable, ITERABLE_KEYWORD):
        return True
    else:
        return False


def pmap(func, iterable, is_skip_check=False):
    if not (is_skip_check or is_iterable(iterable)):
        raise TypeError(f"pmap only accepts iterable, got {type(iterable)}")
    if hasattr(iterable, FUNCTOR_KEYWORD):
        return getattr(iterable, FUNCTOR_KEYWORD)(func)
