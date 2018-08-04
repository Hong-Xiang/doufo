from functools import partial
import numpy as np
from doufo import func



def transpose(t, perm=None):
    return _transpose(t, perm)

@singledispatch
def _transpose(t, perm):
    raise NotImplementedError()

@_transpose.register(np.ndarray)
def _(t, perm=None):
    return np.transpose(t, perm)
