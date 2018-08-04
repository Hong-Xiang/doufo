from typing import Generic, TypeVar, NamedTuple, Sequence, Union, Iterator
from abc import ABCMeta, abstractproperty, abstractmethod
from doufo import Functor, Monoid

T = TypeVar('T')

# TODO add implementation

class Table(Sequence[T], Functor[T], Monoid[T]):
    """
    An unified table access of PyTable/pandas, etc.

    t[0]: 0-th row
    t[0:5] -> Table: [0:5] rows.

    __iter__(self): row iterator

    fmap :: Table -> Table

    """

    def __getitem__(self, i, columns=None) -> Union[T, Table[T]] :
        if isinstance(i, int):
            return self.at_row(i)
        if isinstance(i, slice):
            return self.slice_row(i) 

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        pass

    @abstractmethod
    def at_row(self, i: int) -> T:
        pass
    
    @abstractmethod
    def slice_row(self, s: slice) -> Table[T]:
        pass

    @abstractproperty
    def nb_rows(self) -> int:
        pass
    