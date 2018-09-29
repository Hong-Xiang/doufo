from doufo import singledispatch, multidispatch, method_not_support_msg
import numpy as np
import tensorflow as tf
from .unary_with_args import norm

__all__ = ['all_close', 'matmul', 'project']


@singledispatch(nargs=2, nouts=1)
def all_close(x, y):
    raise TypeError(method_not_support_msg('all_close', x))


@all_close.register(list)
@all_close.register(np.ndarray)
def _(x, y):
    return np.allclose(x, y, atol=1.e-7)


@all_close.register(float)
def _(x, y):
    return abs(x - y) < 1e-7


@multidispatch(nargs=2, nouts=1)
def matmul(x, y):
    return x @ y


@matmul.register(tf.SparseTensor, tf.Tensor)
def _(x, y):
    return tf.sparse_tensor_dense_matmul(x, y)


@multidispatch(nargs=2, nouts=1)
def project(v, n):
    """
    Project Vector v onto plane with normal vector n.
    """
    return v - matmul(v, n) * n / (norm(n) ** 2.0)
