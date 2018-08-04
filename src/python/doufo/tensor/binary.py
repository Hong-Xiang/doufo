from doufo import singledispatch
import numpy as np

__all__ = ['all_close', 'matmul']

@singledispatch
def all_close(x, y):
    raise TypeError


@all_close.register(np.ndarray)
def _(x, y):
    return np.allclose(x, y, atol=1.e-7)

@singledispatch
def matmul(x, y):
    raise TypeError
