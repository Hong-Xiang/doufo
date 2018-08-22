from doufo import singledispatch
from doufo.utils import method_not_support_msg
import numpy as np

__all__ = ['all_close', 'matmul']


@singledispatch
def all_close(x, y):
    raise TypeError(method_not_support_msg('all_close', x))


@all_close.register(list)
@all_close.register(np.ndarray)
def _(x, y):
    return np.allclose(x, y, atol=1.e-7)


@all_close.register(float)
def _(x, y):
    return abs(x - y) < 1e-7


@singledispatch
def matmul(x, y):
    raise TypeError
