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
    new_g = tf.Graph()
    with new_g.as_default():
        con = tf.constant([[1, 2], [3, 4]])

    with tf.Session(graph=new_g) as new_sess:
        assert all_close(new_sess.run(transpose(con)), [[1, 3], [2, 4]])
        assert all_close(new_sess.run(transpose(con, perm=[0, 1])), [[1, 2], [3, 4]])


# TODO
@pytest.mark.skip()
def test_transpose_Variable():
    my_variable = tf.get_variable("my_variable", [1, 1, 1])
    my_variable2 = tf.constant([1, 1, 1])
    with tf.Session() as sess:
        sess.run(my_variable.initializer)

        print(sess.run(transpose(my_variable)))
        print(sess.run(transpose(my_variable2)))


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

#TODO
@pytest.mark.skip()
def test_one_hot():
    pass
#TODO
@pytest.mark.skip()
def test_one_hot_ndarray():
    pass
#TODO
@pytest.mark.skip()
def tests_tf_Tensor():
    new_g = tf.Graph()
    with new_g.as_default():
        con_d = tf.constant([[1, 2], [3, 4]])

    with tf.Session(graph=new_g) as new_sess:
        res = new_sess.run(con_d)
        assert res == 10

def test_split():
    try:
        split('1', '1', '1', '1')
    except Exception as e:
        assert isinstance(e,NotImplementedError)
#TODO(cntk Obsolete)
@pytest.mark.skip()
def test_flatten_cntk():
    pass