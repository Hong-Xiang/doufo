from .tensor import Tensor
from typing import TypeVar
from .binary import matmul
from doufo.tensor import as_scalar
from doufo import multidispatch
from typing import Union
import numpy as np

T = TypeVar('T')

__all__ = ['Vector']


class Vector(Tensor[T]):
    def __init__(self, data):
        super().__init__(data)

    def fmap(self, f):
        return Vector(f(self.unbox()))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @classmethod
    def one_hot(cls, n, l):
        """
        n: position of "hot"
        l: lenght of vector
        """
        v = [0.0] * l
        v[n] = 1.0
        return Vector(v)


def scalar_or_vector_of(result, t):
    return as_scalar(result) if is_result_scalar(t) else Vector(result)


def is_result_scalar(t):
    return isinstance(t, Vector)



