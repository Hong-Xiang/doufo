from typing import Generic, TypeVar, NamedTuple, Sequence, Union, Iterator
from abc import ABCMeta, abstractproperty, abstractmethod
from doufo import Functor, Monoid
from .dataclasses_ import DataArray
from doufo import List

T = TypeVar('T')

# TODO add implementation


class Table(Functor[T], Monoid[T]):
    """
    An unified table access of PyTable/pandas, etc.
    Similar to DataArray, but with following differencies:

    - Prefer lazy, thus before "compute methods" like __getitem__,
    do not perform actual calculation.

    - DataClass infer, automatically create dataclass(optional), 
    if loaded from filesystem.


    t[0]: 0-th row
    t[0:5] -> Table: [0:5] rows.

    __iter__(self): row iterator

    fmap :: Table -> Table
    """
    def __init__(self, source, operations, dataclass=None):
        self.source = source
        self.dataclass = dataclass
    
    def __getitem__(self, i) -> Union[T, Sequence[T]]:
        return self.unbox()[i]

    def __iter__(self) -> Iterator[T]:
        return iter(self.unbox())

    @classmethod
    def empty(cls):
        return cls([])
    
    def extend(self, tb):
        raise NotImplementedError
        # return Table([self.unbox(), tb], self.dataclass)
    
    def unbox(self):
        return self.source 