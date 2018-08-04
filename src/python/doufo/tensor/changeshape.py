from functools import singledispatch, partial
import numpy as np
from doufo import func


def transpose(t, perm=None):
    return _transpose


@transpose.register(np.ndarray)
def _(t, perm=None):
    return np.transpose(t, perm)
