"""
"""

from typing import Iterable, Callable, Optional, TypeVar
from .control import Functor
from .monoid import Monoid
from .function import identity
import itertools
from .on_collections import take_
from functools import partial

__all__ = ['PureIterable', 'IterableElemMap', 'IterableIterMap', 'Count']

T = TypeVar('T')


class PureIterable(Iterable[T], Functor[Iterable[T]], Monoid[Iterable[T]]):
    """doufo.PureIterable: define abstract `Iterable` class inherited from `Iterable`  
    `Function` and `Monoid`. Only iterable, iterator is not PureIterable
    """

class IterableElemMap(PureIterable[T]):
    """doufo.IterableElemMap  
    Attributes:  
        `attr1` (type): Description
    """

    """
    Iterable Functor, fmap functon on elements of iterable.
    Useful for chaining data.
    """
    def __init__(self, source: PureIterable[T], operation=Optional[Callable]):
        self.source = source
        if operation is None:
            operation = identity
        self.operation = operation

    def fmap(self, f):
        return IterableElemMap(self, f)

    def __iter__(self):
        return (self.operation(x) for x in self.source)

    def unbox(self):
        return iter(self)

    @classmethod
    def empty(cls):
        return IterableElemMap(tuple())

    def extend(self, xs: PureIterable[T]):
        return IterableElemMap(IterableIterMap(self).extend(xs))

    def filter(self, f):
        return IterableElemMap(IterableIterMap(self).filter(f))

class IterableIterMap(PureIterable):
    """doufo.IterableIterMap: impl of Iterable Functor, fmap on  
    iterable itself, useful for concatenating, filtering, etc.
    """
    def __init__(self, source: PureIterable, operation=Optional[Callable]):
        """doufo.IterableIterMap.__init__  
        Attributes:  
            `source` (`PureIterable`): an iterable object  
            `operation` (`Optional[Callable]`): `None` or `Callable`,  
            used as the iterator of this object
        """
        self.source = source
        if operation is None:
            operation = identity
        self.operation = operation

    def fmap(self, f):
        # return IterableIterMap(f(self.source), f(self.operation))
        return ItertoolsIterable(self, f)

    def __iter__(self):
        """doufo.IterableIterMap().__iter__: to define `iter()` of   
        this `iterable`
        Args:  
            `self`  
        Returns:  
            return (`IterableIterMap`): next element 
        """
        return (x for x in self.operation(self.source))

    def unbox(self):
        return iter(self)

    def extend(self, xs: PureIterable[T]):
        return self.fmap(lambda s: itertools.chain(s, xs))

    def filter(self, f):
        return self.fmap(partial(filter, f))

    @classmethod
    def empty(cls):
        return IterableIterMap(tuple())


class Count(PureIterable):
    def __init__(self, start=0, step=1):
        self.start = start
        self.step = step

    def __iter__(self):
        return itertools.count(self.start, self.step)


@take_.register(Iterable)
def _(xs: Iterable, n: int)->Iterable:
    return IterableIterMap(xs, itertools.islice(0, n))
