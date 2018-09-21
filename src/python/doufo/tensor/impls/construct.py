import numpy as np
import tensorflow as tf
from scipy.sparse import coo_matrix

# from doufo.tensor import TensorFlowBackend, NumpyBackend
from doufo.tensor import *


@array.register(TensorFlowBackend)
def _(shape, dtype, name):
    return tf.get_variable(name, shape, dtype)


@array.register(NumpyBackend)
def _(shape, dtype, name=None):
    return np.zeros(shape, dtype)


@sparse.register(TensorFlowBackend)
def _(data, name=None):
    if isinstance(data, np.ndarray):
        return tf.SparseTensor(data[:, :-1], data[:, -1], data.shape)
    if isinstance(data, coo_matrix):
        return tf.SparseTensor(np.array([data.row, data.col]).T, data.data)


@copy.register(NumpyBackend)
@copy.register(np)
def _(data):
    return np.array(data)


@const.register(TensorFlowBackend)
@const.register(tf)
def _(data, dtype=None, shape=None, name=None):
    return tf.constant(data, dtype, shape, name=name)
