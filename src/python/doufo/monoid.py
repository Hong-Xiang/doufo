from abc import ABC, abstractmethod, abstractclassmethod
from typing import Generic, TypeVar, Iterable, Sequence
import functools
import operator


__all__ = ['Monoid']

T = TypeVar('T')


class Monoid(Generic[T]):
    @abstractclassmethod
    def empty(self) -> 'Monoid[T]':
        pass

    @abstractmethod
    def extend(self, x: 'Monoid[T]') -> 'Monoid[T]':
        pass

    def __add__(self, x: 'Monoid[T]') -> 'Monoid[T]':
        return self.extend(x)
