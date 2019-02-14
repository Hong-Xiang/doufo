from doufo.tensor.unary_with_args import *
from doufo.tensor.binary import *
import tensorflow as tf
import numpy as np
import pytest


def test_transpose():
    try:
        transpose('1')
    except Exception as e:
        assert isinstance(e, NotImplementedError)


def test_transpose_ndarray():
    assert all_close(transpose(np.array([[1, 2], [3, 4]])), [[1, 3], [2, 4]])
    assert all_close(transpose(np.array([[1, 2], [3, 4]]), perm=[1, 0]), [[1, 3], [2, 4]])


def test_transpose_Tensor():
    with tf.Graph().as_default():
        con = tf.constant([[1, 2], [3, 4]])

        with tf.Session() as new_sess:
            assert all_close(new_sess.run(transpose(con)), [[1, 3], [2, 4]])
            assert all_close(new_sess.run(transpose(con, perm=[0, 1])), [[1, 2], [3, 4]])


def test_transpose_Variable():
    with tf.Graph().as_default():
        my_variable = tf.get_variable("my_variable", [0, 0, 0])

        with tf.Session() as new_sess:
            new_sess.run(my_variable.initializer)
            assert list(new_sess.run(transpose(my_variable))) == []


def test_norm():
    try:
        norm('1')
    except Exception as e:
        assert isinstance(e, TypeError)


def test_norm_ndarray():
    assert all_close(norm(np.array([-4, -3, -2, -1, 0, 1, 2, 3, 4])), 7.745966692414834)


def test_norm_list():
    assert all_close(norm([-4, -3, -2, -1, 0, 1, 2, 3, 4]), 7.745966692414834)


def test_flatten():
    try:
        flatten('1')
    except Exception as e:
        assert isinstance(e, NotImplementedError)


def test_flatten_tf_Tensor():
    new_g = tf.Graph()
    with new_g.as_default():
        t1 = tf.constant([[[1, 2], [3, 4]]])
        t2 = tf.constant([[1, 2], [3, 4]])
    with tf.Session(graph=new_g) as new_sess:
        assert new_sess.run(flatten(t1)).shape == (1, 4)
        assert new_sess.run(flatten(t2)).shape == (2, 2)


def test_flatten_ndarray():
    assert flatten(np.array([[1, 2], [3, 4]])).shape == (2, 2)
    assert flatten(np.array([[[1, 2], [3, 4]]])).shape == (1, 4)


def test_flatten_ndarray2():
    try:
        flatten(np.array([[1, 2], [3, 4]]), 1)
    except Exception as e:
        assert isinstance(e, NotImplementedError)
        assert e == """"Flatten for numpy Tensor with batch_dim != 0 is not implemented yet")"""


@pytest.fixture()
def one_hot_result():
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0]])


def test_one_hot(one_hot_result):
    class T():
        def __init__(self, x: int, y: int, z: int):
            self._ = np.array([x, y, z])

        def fmap(self, x):
            _ = self._
            return x(_)

    t = T(0, 1, 2)
    assert all_close(one_hot(t, 4), one_hot_result)


def test_one_hot_npy(one_hot_result):
    assert all_close(one_hot(np.array([0, 1, 2]), 4), one_hot_result)


def test_one_hot_tf_Tensor():
    def one_hot_result():
        return np.array([[[0, 1, 0, 0, ],
                          [0, 0, 1, 0, ]],

                         [[0, 0, 0, 1, ],
                          [0, 0, 0, 0, ]]])

    with tf.Graph().as_default():
        t = tf.constant([[1, 2], [3, 4]])

        with tf.Session() as new_sess:
            assert all_close(new_sess.run(one_hot(t, 4)), one_hot_result())


def test_split():
    try:
        split('1', '1', '1', '1')
    except Exception as e:
        assert isinstance(e, NotImplementedError)


# TODO(cntk Obsolete)
@pytest.mark.skip()
def test_flatten_cntk():
    pass
