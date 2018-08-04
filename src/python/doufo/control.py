from typing import Generic, TypeVar, Callable
from abc import abstractmethod, ABCMeta

A = TypeVar('A')
B = TypeVar('B')

__all__ = ['Functor', 'Monad']

class Functor(Generic[A], metaclass=ABCMeta):
    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
        pass

    @abstractmethod
    def unbox(self) -> A:
        pass


class Monad(Functor[A]):
    def __rshift__(self, f: Callable[[A], 'Monad[B]']) -> 'Monad[B]':
        """ Alias to bind """
        return self.bind(f)

    @abstractmethod
    def fmap(self, f: Callable[[A], B]) -> 'Monad[B]':
        pass

    @abstractmethod
    def bind(self, f: Callable[[A], 'Monad[B]']) -> 'Monad[B]':
        pass


