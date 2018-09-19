from functools import partial
import numpy as np
import tensorflow as tf

from doufo import singledispatch

__all__ = ['transpose', 'norm', 'flatten', 'one_hot', 'split']


@singledispatch(nargs=2, nouts=1)
def transpose(t, perm=None):
    raise NotImplementedError(f"No transpose implementation for {type(t)}")


@transpose.register(np.ndarray)
def _(t, perm=None):
    return np.transpose(t, perm)


@transpose.register(tf.Tensor)
@transpose.register(tf.Variable)
def _(t, perm=None):
    return tf.transpose(t, perm)


@singledispatch(nouts=1)
def norm(t, p=2.0):
    raise TypeError()


@norm.register(np.ndarray)
def _(t, p=2.0):
    return np.linalg.norm(t)


@norm.register(list)
def _(t, p=2.0):
    return norm(np.array(t))


@singledispatch(nargs=2, nouts=1)
def flatten(t, batch_sim=0):
    raise NotImplementedError()


@flatten.register(tf.Tensor)
def _(t, batch_dim=0):
    return tf.keras.layers.Flatten()(t)


@flatten.register(np.ndarray)
def _(t, batch_dim=0):
    if batch_dim == 0:
        return t.reshape([t.shape[0], -1])
    raise NotImplementedError(
        "Flatten for numpy Tensor with batch_dim != 0 is not implemented yet")


# TODO add sparse support

@singledispatch(nargs=2, nouts=1)
def one_hot(t, nb_classes):
    return t.fmap(lambda _: one_hot(_, nb_classes))


@one_hot.register(np.ndarray)
def _(t, nb_classes):
    result = np.zeros(list(t.shape) + [nb_classes])
    result[np.arange(t.size), t] = 1
    return result


@one_hot.register(tf.Tensor)
def _(t, nb_classes):
    return tf.keras.backend.one_hot(t, nb_classes)


@singledispatch(nargs=4, nouts=1)
def split(t, nb_partition, id_partition, axis=0):
    raise NotImplementedError


try:
    import cntk
except ImportError:
    pass
else:
    @flatten.register(cntk.Variable)
    def _(t, batch_dim=0):
        return cntk.squeeze(cntk.flatten(t, axis=batch_dim))


    @one_hot.register(cntk.Variable)
    def _(t, nb_classes):
        return cntk.one_hot(t, nb_classes)
