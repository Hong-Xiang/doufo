"""
Functor is base class for the generic functors.
A composite function can be obtain by the fmap method.
Usually the PureFunction class is used to implement this rather than the basic functor class.

Monad: to be added
"""
from __future__ import annotations

from typing import Generic, TypeVar, Callable
from abc import abstractmethod, ABCMeta
import functools
import toolz.functoolz as functoolz

A = TypeVar("A")
B = TypeVar("B")

__all__ = ["Functor", "Monad"]


class Functor(Generic[A], metaclass=ABCMeta):
    """
        Abstract class of `Functor`s. A `Functor` represents a type that can 
        be mapped over.

        Need to satisfy:
            x.map(identity) == identity(x)
            x.map(compose(f, g)) == x.map(f).map(g)
    """

    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> Functor[B]:
        """
            `fmap` applies a function (`Callable[[A], B]`) to all its inputs (`[A]').

            :param `f`: a callable function with inputs `[A]` and output 'B'

            :return: `Functor[B]`: a set of object of this class
        """
        ...

    @abstractmethod
    def unbox(self) -> A:
        """
            Abstract method of `unbox` in class Functor

            :return: un-wrapped raw tensor.
        """
        pass


class Monad(Functor[A]):
    """
        A monad can be thought as a composable computation description. It is 
        a child class of `Functor` who pluses a binding feature. 
    """

    def __rshift__(self, f: Callable[[A], Monad[B]]) -> Monad[B]:
        """
            overwrite `>>` in Python to alias bind. For example: `(g>>f)(*) = g(f(*))`

            :param `f`: A callable function with output `Monad[B]`
        """
        return self.bind(f)

    def fmap(self, f: Callable[[A], B]) -> Monad[B]:
        """
            `fmap` applies a function: (x: A) => B to all its inputs (`[A]').

            :param `f`: a callable function with inputs `[A]` and output 'B'

            :return: `Monad[B]`: a set of object of this class
        """
        return self.bind(lambda x: self.__class__(f(x)))

    @abstractmethod
    def bind(self, f: Callable[[A], Monad[B]]) -> Monad[B]:
        """
            To support function composition. for example `g(f(*)) = p(*)` where
            `p = g.bind(f)`
        """
        ...

    def pipe(self, *functions):
        return functools.reduce(lambda m, f: m.bind(f), functions, self)

    def __join__(self):
        return self.bind(functoolz.identity)
