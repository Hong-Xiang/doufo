import numpy as np
import tensorflow as tf
from doufo import singledispatch, multidispatch, tagfunc

DEFAULT_CONSTRUCTOR = np.array

__all__ = ['to_tensor_like', 'array', 'const', 'copy', 'sparse']


@singledispatch()
def to_tensor_like(t):
    return DEFAULT_CONSTRUCTOR(t)


@to_tensor_like.register(np.ndarray)
@to_tensor_like.register(tf.Tensor)
def _(t):
    return t


@tagfunc(nouts=1)
def array(shape, dtype, name=None):
    """
    Construct multi dimensional array for specific backend
    :return: constructed array.
    """
    raise NotImplementedError


@tagfunc(nouts=1)
def sparse(data, name=None):
    raise NotImplementedError


@tagfunc(nouts=1)
def const(data, dtype=None, shape=None, name=None):
    raise NotImplementedError


@tagfunc(nouts=1)
def copy(data):
    raise NotImplementedError
