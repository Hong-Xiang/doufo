"""
Objective:

Lazy "concatenated" lists/table or other Sequence[T], thus combining 
multiple sequences without actually concatenating them. 
"""
from doufo import Functor, Monoid, List
from typing import Sequence, TypeVar, Callable
from itertools import chain

T = TypeVar('T')
B = TypeVar('B')


class CompositeSequence(Sequence[T], Functor[T], Monoid[T]):
    """
    Virtual concatenated sequence, for used in some high-cost concatenate, like merging multiple HDF5 files into
    one "virtual" table.
    """

    def __init__(self, sources: List[Sequence[T]]):
        self.sources = List(sources)

    def __getitem__(self, s):
        id_source, s = index_and_new_slice(self.sources, s)
        return self.sources[id_source][s]

    def __iter__(self):
        return chain(*self.unbox())

    def __len__(self):
        return sum(map(len, self.unbox()))

    def unbox(self):
        return self.sources

    def extend(self, x: 'Monoid[T]'):
        return CompositeSequence(List(self.sources).extend([x]))

    def fmap(self, f: Callable[[T], B]):
        return CompositeSequence(self.sources.fmap(lambda s: s.fmap(f)))


def index_and_new_slice(source, s):
    if isinstance(s, int):
        acc, idx = 0, 0
        while acc < s:
            if acc + len(source[idx]) > s:
                break
            acc += len(source[idx])
            idx += 1
        return idx, s - acc
    raise TypeError("slice is not supported yet, getitem is works with int only.")
