from doufo import Functor
from collections import UserDict
from typing import TypeVar

T = TypeVar('T')

__all__ = ['Dict']

class Dict(UserDict, Functor[T]):
    def fmap(self, f):
        return Dict({k: f(v) for k, v in self.items()})

    def unbox(self):
        return self.data