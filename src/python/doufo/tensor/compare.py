from functools import singledispatch
from doufo.tensor import Tensor
from doufo import func
import numpy as np


@func
def all_close(x, y):
    return _all_close(x, y)


@singledispatch
def _all_close(x, y):
    raise TypeError


@_all_close.register(np.ndarray)
def _(x, y):
    return np.allclose(x, y, atol=1.e-7)
