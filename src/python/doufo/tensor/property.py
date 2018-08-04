from functools import singledispatch
from dxl.data.tensor import Tensor
import numpy as np
import tensorflow as tf
from dxl.data import List
from dxl.function.utils import method_not_support_msg

__all__ = ['shape', 'ndim', 'argmax']


@singledispatch
@func
def shape(t) -> List[int]:
    raise TypeError(method_not_support_msg(t, "shape"))


@shape.register(Tensor)
@shape.register(np.ndarray)
def _(t) -> List[int]:
    return List(t.shape)


@shape.register(tf.Tensor)
def _(t) -> List[int]:
    return List(t.shape.as_list())


@singledispatch
def ndim(t) -> int:
    raise TypeError(method_not_support_msg(t, "ndim"))


@ndim.register(Tensor)
@ndim.register(np.ndarray)
def _(t) -> List[int]:
    return t.ndim


@singledispatch
def size(t) -> int:
    raise TypeError(method_not_support_msg(t, "size"))


@size.register(Tensor)
@size.register(np.ndarray)
def _(t) -> List[int]:
    return t.size


@singledispatch
def argmax(t):
    raise TypeError(method_not_support_msg(t, "argmax"))


@argmax.register(Tensor)
def _(t):
    return argmax(t.join())


@argmax.register(np.ndarray)
def _(t):
    return np.argmax(t)
