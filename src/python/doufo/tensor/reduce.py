from functools import singledispatch
import numpy as np
from functools import singledispatch
from dxl.data.tensor import Tensor

__all__ = ['sum_', 'norm', 'is_scalar']


@singledispatch
def sum_(t):
    raise TypeError


@sum_.register(np.ndarray)
def _(t):
    return np.sum(t)


@sum_.register(Tensor)
def _(t):
    return sum_(t.join())


@singledispatch
def norm(t, *, p=2.0):
    return np.linalg.norm(t)


@norm.register(np.ndarray)
def _(t, *, p=2.0):
    return np.linalg.norm(t)


@norm.register(Tensor)
def _(t, *, p=2.0):
    return norm(t.join())


@norm.register(list)
def _(t, *, p=2.0):
    return norm(np.array(t))


@singledispatch
def is_scalar(t):
    return np.isscalar(t)


@is_scalar.register(int)
@is_scalar.register(float)
@is_scalar.register(np.int32)
@is_scalar.register(np.int64)
@is_scalar.register(np.float32)
@is_scalar.register(np.float64)
def t(t):
    return True


@is_scalar.register(np.ndarray)
def _(t):
    return np.isscalar(t)


@is_scalar.register(Tensor)
def _(t):
    return is_scalar(t.join())
