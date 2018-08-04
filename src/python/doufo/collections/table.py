from typing import Generic, TypeVar, NamedTuple, Sequence, Union, Iterator
from abc import ABCMeta, abstractproperty, abstractmethod
from doufo import Functor, Monoid

a = TypeVar('a')

# TODO add implementation

class Table(Functor[a], Monoid[a], Sequence[a]):
    """
    An unified table access of PyTable/pandas, etc.

    t[0]: 0-th row
    t[0:5] -> Table: [0:5] rows.

    __iter__(self): row iterator

    fmap :: Table -> Table

    """

    def __getitem__(self, i, columns=None) -> Union[a, Table[a]] :
        if isinstance(i, int):
            return self.at_row(i)
        if isinstance(i, slice):
            return self.slice_row(i) 

    @abstractmethod
    def __iter__(self) -> Iterator[a]:
        pass

    @abstractmethod
    def at_row(self, i: int) -> a:
        pass
    
    @abstractmethod
    def slice_row(self, s: slice) -> Table[a]:
        pass

    @abstractproperty
    def nb_rows(self) -> int:
        pass
    