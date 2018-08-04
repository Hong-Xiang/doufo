from functools import singledispatch
import numpy as np
import tensorflow as tf
from doufo.tensor import Tensor
from doufo import func

DEFAULT_CONSTRUCTOR = np.array

__all__ = ['to_tensor_like']


@func
def to_tensor_like(t):
    return _to_tensor_like(t)

@singledispatch
def _to_tensor_like(t):
    return DEFAULT_CONSTRUCTOR(t)

@to_tensor_like.register(np.ndarray)
@to_tensor_like.register(tf.Tensor)
def _(t):
    return t


