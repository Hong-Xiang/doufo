from doufo import singledispatch
import numpy as np
import tensorflow as tf

__all__ = ['sum_', 'norm', 'is_scalar', 'argmax']


@singledispatch(nargs=2, ndefs=1, nouts=1)
def sum_(t, axis=None):
    return t.fmap(lambda _: sum_(_, axis))


@sum_.register(list)
def _(t, axis=None):
    return sum(t)


@sum_.register(np.ndarray)
def _(t, axis=None):
    return np.sum(t, axis=axis)


@sum_.register(tf.Tensor)
def _(x, axis=None):
    return tf.reduce_sum(x, axis=axis)


@singledispatch()
def norm(t, p=2.0):
    return np.linalg.norm(t)


@singledispatch()
def is_scalar(t):
    return np.isscalar(t)


@is_scalar.register(int)
@is_scalar.register(float)
@is_scalar.register(np.int32)
@is_scalar.register(np.int64)
@is_scalar.register(np.float32)
@is_scalar.register(np.float64)
def t(t):
    return True


@is_scalar.register(np.ndarray)
def _(t):
    return np.isscalar(t)


@singledispatch(nargs=2, nouts=1, ndefs=1)
def argmax(t, axis=None):
    return t.fmap(lambda _: argmax(_, axis))


@argmax.register(np.ndarray)
def _(x, axis=None):
    return np.argmax(x, axis=axis)


@argmax.register(tf.Tensor)
def _(x, axis=None):
    return tf.argmax(x, axis=axis)
