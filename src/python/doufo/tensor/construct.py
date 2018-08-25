import numpy as np
import tensorflow as tf
from doufo import singledispatch, multidispatch
from .backends import TensorFlowBackend, CNTKBackend, NumpyBackend

DEFAULT_CONSTRUCTOR = np.array

__all__ = ['to_tensor_like', 'array', 'const', 'copy', 'sparse']


@singledispatch()
def to_tensor_like(t):
    return DEFAULT_CONSTRUCTOR(t)


@to_tensor_like.register(np.ndarray)
@to_tensor_like.register(tf.Tensor)
def _(t):
    return t


@singledispatch(nargs=4, nouts=1)
def array(backend, shape, dtype, name=None):
    """
    Construct multi dimensional array for specific backend
    :return: constructed array.
    """
    raise NotImplementedError


@multidispatch(nargs=5, nouts=1)
def sparse(backend, data, shape, dtype, name=None):
    raise NotImplementedError

@singledispatch()
def const(source, backend=None, name=None):
    raise NotImplementedError


@singledispatch(nargs=3, nouts=1)
def copy(source, backend=None, name=None):
    raise NotImplementedError


@copy.register(np)
@copy.register(np.ndarray)
def _(source, backend=None, name=None):
    return np.array(source)
