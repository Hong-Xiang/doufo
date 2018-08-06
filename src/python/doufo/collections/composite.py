"""
Objective:

Lazy "concatenated" lists/table or other Sequence[T], thus combining 
multiple sequences without actually concatenating them. 
"""
from doufo import Functor, Monoid
from typing import Sequence, TypeVar
from itertools import chain

T = TypeVar('T')

class CompositeSequence(Sequence[T], Functor[T], Monoid[T]):
    def __init__(self, sources):
        self.sources = sources
    
    def __getitem__(self, s):
        # TODO implementation
        ...
    
    def __iter__(self):
        return chain(*self.unbox()) 
    
    def __len__(self):
        return sum(map(len, self.unbox()))
    
    def unbox(self):
        return self.sources
