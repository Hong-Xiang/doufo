from functools import partial
import numpy as np
import tensorflow as tf
import cntk
from doufo import singledispatch

__all__ = ['transpose', 'norm', 'flatten']


@singledispatch(nargs=2, nouts=1)
def transpose(t, perm=None):
    raise NotImplementedError()


@transpose.register(np.ndarray)
def _(t, perm=None):
    return np.transpose(t, perm)


@transpose.register(tf.Tensor)
def _(t, perm=None):
    return tf.transpose(t, perm)


@singledispatch(nargs=2, nouts=1)
def norm(t, p=2.0):
    raise TypeError()


@norm.register(np.ndarray)
def _(t, p=2.0):
    return np.linalg.norm(t)


@norm.register(list)
def _(t, p=2.0):
    return norm(np.array(t))


@singledispatch(nargs=2, nouts=1)
def flatten(x, batch_sim=0):
    raise NotImplementedError()


@flatten.register(tf.Tensor)
def _(x, batch_dim=0):
    return tf.keras.layers.Flatten()(x)


@flatten.register(cntk.Variable)
def _(x, batch_dim=0):
    return cntk.squeeze(cntk.flatten(x, axis=batch_dim))


@flatten.register(np.ndarray)
def _(x, batch_dim=0):
    if batch_dim == 0:
        return x.reshape([x.shape[0], -1])
    raise NotImplementedError(
        "Flatten for numpy Tensor with batch_dim != 0 is not implemented yet")
