from doufo.tensor import *
import numpy as np
import tensorflow as tf
import pytest
import cntk as C


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


@pytest.fixture()
def one_hot_result():
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0]])


def test_one_hot_npy(one_hot_result):
    assert all_close(one_hot(np.array([0, 1, 2]), 4), one_hot_result)


@pytest.mark.skip("slow")
def test_one_hot_cntk(one_hot_result):
    x = C.input_variable([], np.float32)
    y = one_hot(x, 4)
    result = y.eval({x: np.array([0, 1, 2], np.float32)})
    assert all_close(result, one_hot_result)


def test_one_hot_tensorflow(tensorflow_test_session, one_hot_result):
    x = tf.constant([0, 1, 2])
    y = one_hot(x, 4)
    assert all_close(tensorflow_test_session.run(y), one_hot_result)


def test_sum_numpy():
    assert sum_(np.array([1, 2, 3])) == 6


def test_sum_tensorflow(tensorflow_test_session):
    assert tensorflow_test_session.run(sum_(tf.constant([1, 2, 3]))) == 6
