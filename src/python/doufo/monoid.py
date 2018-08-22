from abc import abstractmethod
from typing import Generic, TypeVar

__all__ = ['Monoid']

T = TypeVar('T')


class Monoid(Generic[T]):
    '''
    Describe the objects that surpport associative operation.
    e.g. the addition of lists. ([1,2] + [3,4]) + [5,6] = [1,2] + ([3,4] + [5,6])
    '''
    @classmethod
    @abstractmethod
    def empty(cls) -> 'Monoid[T]':
        pass

    @abstractmethod
    def extend(self, x: 'Monoid[T]') -> 'Monoid[T]':
        pass

    def __add__(self, x: 'Monoid[T]') -> 'Monoid[T]':
        return self.extend(x)
