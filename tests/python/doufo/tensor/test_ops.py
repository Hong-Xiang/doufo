from doufo.tensor import *
import numpy as np
import tensorflow as tf
import pytest


@pytest.fixture()
def tftest():
    with tf.Graph().as_default():
        yield


def test_shape_numpy():
    x = np.ones([3, 3, 3])
    assert shape(x) == [3, 3, 3]


def test_shape_tensorflow(tftest):
    x = tf.constant(np.ones([3, 3, 3]))
    assert shape(x) == [3, 3, 3]


def test_shape_tensorflow_placeholder(tftest):
    x = tf.placeholder(tf.float32, [None, 3, 3])
    assert shape(x) == [None, 3, 3]
