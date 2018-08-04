from functools import singledispatch
from dxl.data.tensor import Tensor
import numpy as np

__all__ = ['abs_', 'unit', 'as_scalar']


@singledispatch
def abs_(t):
    raise TypeError()





@abs_.register(np.ndarray)
def _(t):
    return np.abs(t)


@singledispatch
def unit(t):
    raise TypeError


@unit.register(np.ndarray)
def _(t):
    return t / np.linalg.norm(t)


@singledispatch
def as_scalar(t):
    raise TypeError()


@as_scalar.register(np.ndarray)
def _(t):
    return np.asscalar(t)


@singledispatch
def square(t):
    raise TypeError


@square.register(np.ndarray)
def _(t):
    return np.square(t)


@as_scalar.register(int)
@as_scalar.register(float)
@as_scalar.register(np.int32)
@as_scalar.register(np.int64)
@as_scalar.register(np.float32)
@as_scalar.register(np.float64)
def _(t):
    return t
