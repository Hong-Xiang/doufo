"""
Functor is base class for the generic functors.
A composite function can be obtain by the fmap method.
Usually the PureFunction class is used to implement this rather than the basic functor class.

Monad: to be added
"""

from typing import Generic, TypeVar, Callable
from abc import abstractmethod, ABCMeta

A = TypeVar('A')
B = TypeVar('B')

__all__ = ['Functor', 'Monad']


class Functor(Generic[A], metaclass=ABCMeta):
    """
    Functor class is the abstract base class of all functors, which defines a set of \
    functions those satify the properties of functors, who transfer a Category to \
    another Category:
    A functor F has to provide the capablitities:
    1. morphism from A to F[A]
    2. morphism form f: A->B to F[f]: F[A]->F[B]
    In fact, the method 'map' is to provide the capablity
    -----------------------------------------------------------------------
    A:C
    F[A]:D
    f:A->B
    map(f): F[A]->F[B]
    """

    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
        pass

    @abstractmethod
    def unbox(self) -> A:
        pass


class Monad(Functor[A]):
    """
    A monad is a functor who provide one more capablity, which is bind
    A monad has to provide:
    1. morphism from A to M[A]
    2. morphism form f: A->B to M[f]: M[A]->M[B]
    3. flatten: M[M[A]] -> M[A]
    'flatMap' is flatten&Map indeed.
    -----------------------------------------------------------------------
    A:C
    M[A]:D
    f:A->B
    map(M): M[A]->M[B]
    g:A->M[B]
    flatMap(g):M[A]->M[B]
    flatten:M[M[A]]->M[A]
    """

    def __rshift__(self, f: Callable[[A], 'Monad[B]']) -> 'Monad[B]':
        """ Alias to bind """
        return self.bind(f)

    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> 'Monad[B]':
        pass

    @abstractmethod
    def bind(self, f: Callable[[A], 'Monad[B]']) -> 'Monad[B]':
        pass
