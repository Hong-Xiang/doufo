from typing import Iterable, Callable, Optional
from .control import Functor
from .function import identity
import itertools
from .on_collections import take_

__all__ = ['PureIterable', 'IterableElemMap', 'IterableIterMap', 'Count']


class PureIterable(Iterable, Functor[Iterable]):
    """
    Only iterable, iterator is not PureIterable
    """


class IterableElemMap(PureIterable):
    def __init__(self, source: PureIterable, opeartion=Optional[Callable]):
        self.source = source
        if opeartion is None:
            opeartion = identity
        self.opeartion = opeartion

    def fmap(self, f):
        return IterableElemMap(self, f)

    def __iter__(self):
        return (self.opeartion(x) for x in self.source)

    def unbox(self):
        return iter(self)


class IterableIterMap(PureIterable):
    def __init__(self, source: PureIterable, opeartion=Optional[Callable]):
        self.source = source
        self.opeartion = opeartion

    def fmap(self, f):
        return ItertoolsIterable(self, f)

    def __iter__(self):
        return (x for x in self.opeartion(self.source))

    def unbox(self):
        return iter(self)


class Count(PureIterable):
    def __init__(self, start=0, step=1):
        self.start = start
        self.step = step

    def __iter__(self):
        return itertools.count(self.start, self.step)


@take_.register(Iterable)
def _(xs:Iterable, n:int)->Iterable:
    return IterableIterMap(xs, itertools.islice(0, n))
