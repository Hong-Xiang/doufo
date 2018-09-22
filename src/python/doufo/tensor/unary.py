import numpy as np
import tensorflow as tf
from doufo import List, singledispatch, method_not_support_msg


"""
Provides the basic operation for unarray-like data.

Example:
    shape: return the shape of input data.
"""
__all__ = ['shape', 'ndim', 'size', 'abs_', 'unit', 'as_scalar', 'square', 'argmax']


@singledispatch()
def shape(t) -> List[int]:
    raise TypeError(method_not_support_msg(shape, t))


@shape.register(np.ndarray)
def _(t) -> List[int]:
    return List(t.shape)


@shape.register(tf.Tensor)
def _(t) -> List[int]:
    return List(t.shape.as_list())


@singledispatch()
def ndim(t) -> int:
    raise TypeError(method_not_support_msg(ndim, t))


@ndim.register(np.ndarray)
def _(t) -> List[int]:
    return t.ndim


@singledispatch()
def size(t) -> int:
    raise TypeError(method_not_support_msg(size, t))


@size.register(np.ndarray)
def _(t) -> List[int]:
    return t.size


@singledispatch()
def argmax(t):
    raise TypeError(method_not_support_msg(argmax, t))


@argmax.register(np.ndarray)
def _(t):
    return np.argmax(t)


@singledispatch()
def abs_(t):
    raise TypeError()


@abs_.register(np.ndarray)
def _(t):
    return np.abs(t)


@singledispatch()
def unit(t):
    raise TypeError(f"{type(t)}")


@unit.register(np.ndarray)
def _(t):
    return t / np.linalg.norm(t)


@singledispatch()
def as_scalar(t):
    raise TypeError()


@as_scalar.register(np.ndarray)
@as_scalar.register(np.bool_)
def _(t):
    return np.asscalar(t)


@singledispatch()
def square(t):
    raise TypeError


@square.register(np.ndarray)
def _(t):
    return np.square(t)


@as_scalar.register(int)
@as_scalar.register(float)
@as_scalar.register(np.int32)
@as_scalar.register(np.int64)
@as_scalar.register(np.float32)
@as_scalar.register(np.float64)
@as_scalar.register(bool)
def _(t):
    return t
