from doufo.tensor.unary_reduce import *
import numpy as np
import tensorflow as tf
from doufo.tensor import all_close

def test_sum_():
    class A():
        def __init__(self, x: int, y: int) -> list:
            self._ = [x, y]

        def fmap(self, x):
            _ = self._
            return x(_)

    a = A(1, 2)
    assert sum_(a) ==  3


def test_sum_list():
    assert sum_([1, 2]) == 3


def test_sum_ndarry():
    assert sum_(np.array([[1, 2], [3, 4]])) == 10


def test_sum_Tensor():
    new_g = tf.Graph()
    with new_g.as_default():
        con_d = tf.constant([[1, 2], [3, 4]])

    with tf.Session(graph=new_g) as new_sess:
        res = new_sess.run(sum_(con_d))
        assert res == 10


def test_norm():
    tuple = (-4, -3, -2, -1, 0, 1, 2, 3, 4)
    assert all_close(norm(tuple) , 7.745966692414834)


def test_is_scalar():
    assert is_scalar(np.string_('string')) == True
    assert is_scalar([1]) == False


def test_is_scalar_int_float_int32_int64_float32_float64():
    assert is_scalar(1) == True
    assert is_scalar(1.0) == True
    assert is_scalar(np.int32(1)) == True
    assert is_scalar(np.int64(1)) == True
    assert is_scalar(np.float32(1.0)) == True
    assert is_scalar(np.float64(1.0)) == True


def test_is_scalar_ndarray():
    assert is_scalar(np.array([1])) == False


def test_argmax():
    class Foo():
        def __init__(self, data):
            self.data = data

        def fmap(self, f):
            return f(np.array(self.data))

    foo = Foo([[1, 2], [3, 4], [6, 5]])
    assert list(argmax(foo, 1)) == [1, 1, 0]
    assert list(argmax(foo, 0)) == [2, 2]
    assert argmax(foo) == 4


def test_ndarry():
    ndarray_data = np.array([[1, 2], [3, 4], [6, 5]])
    assert list(argmax(ndarray_data, 1)) == [1, 1, 0]
    assert list(argmax(ndarray_data, 0)) == [2, 2]
    assert argmax(ndarray_data) == 4


def test_tf_Tensor():
    new_g = tf.Graph()
    with new_g.as_default():
        con_d = tf.constant([[1, 2], [3, 4], [6, 5]])

    with tf.Session(graph=new_g) as new_sess:
        assert list(new_sess.run(argmax(con_d, 1))) == [1, 1, 0]
        assert list(new_sess.run(argmax(con_d, 0))) == [2, 2]
        assert list(new_sess.run(argmax(con_d))) == [2, 2]
