from functools import partial
import numpy as np
from doufo import singledispatch

__all__ = ['transpose', 'norm']

@singledispatch
def transpose(t, perm=None):
    raise NotImplementedError()

@transpose.register(np.ndarray)
def _(t, perm=None):
    return np.transpose(t, perm)

@singledispatch
def norm(t, p=2.0):
    raise TypeError()

@norm.register(np.ndarray)
def _(t, p=2.0):
    return np.linalg.norm(t)

@norm.register(list)
def _(t, p=2.0):
    return norm(np.array(t))