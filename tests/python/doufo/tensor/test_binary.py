from doufo.tensor import Vector
from doufo.tensor.binary import *
import numpy as np
import tensorflow as tf
import pytest


def test_all_close():
    try:
        all_close(1, 1)
    except Exception as f:
        assert isinstance(f, TypeError)


def test_all_close_ndarray():
    x = np.array([[1, 2], [3, 4]])
    y = np.array([[1, 2], [3, 4]])
    assert all_close(x, y) == True


def test_all_close_float():
    x = 0.1
    y = 0.2
    assert all_close(x, y) == False
    x = 0.0000000001
    y = 0.0000000002
    assert all_close(x, y)


def test_matmul_SparseTensor_Tensor():
    st = tf.SparseTensor(values=[1, 2], indices=[[0, 0], [1, 1]], dense_shape=[2, 2])
    t = tf.ones(shape=[2, 2], dtype=tf.int32)

    res = matmul(st, t)
    with tf.Session() as sess:
        assert all_close(sess.run(res), np.array([[1, 1], [2, 2]]))


def test_project():
    v = Vector([[1, 1], [1, 1]])
    n = np.array([[1, 1], [1, 1]])

    assert all_close(project(v, n) == np.array([[0.5, 0.5], [0.5, 0.5]]))
