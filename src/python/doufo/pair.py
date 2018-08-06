from abc import ABC, abstractproperty
from .control import Functor
from doufo import dataclass
from typing import Generic, TypeVar, Callable, Union, Tuple
import operator
import attr


A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')


# @attr.s(frozen=True, auto_attribs=True)
@dataclass
class Pair(Functor[Tuple[A, B]], Generic[A, B]):
    """
    Base class with two elements.
    """
    fst: A
    snd: B
    # def __init__(self, fst: A, snd: B):
        # self.fst = fst
        # self.snd = snd

    def fmap(self, f: Callable[[A, B], Tuple[C, D]]) -> 'Pair[C, B]':
        return Pair(*f(self.fst, self.snd))

    def fmap2(self, f: Callable[[Union[A, B]], C]) -> 'Pair[C, C]':
        return (self.fmap(lambda fst, snd: (f(fst), snd))
                .fmap(lambda fst, snd: (fst, f(snd))))

    def flip(self) -> 'Pair[B, A]':
        return Pair(self.snd, self.fst)

    def unbox(self):
        return (self.fst, self.snd)
