from doufo.tensor.unary import *
import numpy as np
import tensorflow as tf
from doufo.tensor import all_close


def test_shape():
    try:
        shape('1')
    except Exception as e:
        assert e is not None
        assert isinstance(e, TypeError)


def test_shape_ndarry():
    assert shape(np.array([[1, 2], [1, 2]])) == [2, 2]


def test_shape_Tensor():
    with tf.Graph().as_default():
        assert shape(tf.constant([1, 2])) == list((2,))
        assert shape(tf.constant([[1, 2], [3, 4]])) == list((2, 2))


def test_ndim():
    try:
        ndim('1')
    except Exception as e:
        assert isinstance(e, TypeError)


def test_ndim_ndarry():
    assert ndim(np.array([[1, 2], [3, 4]])) == 2


def test_size():
    try:
        size('1')
    except Exception as e:
        assert isinstance(e, TypeError)


def test_size_ndarry():
    assert size(np.array([[1, 2], [3, 4]])) == 4


def test_argmax():
    try:
        argmax('1')
    except Exception as e:
        assert isinstance(e, TypeError)


def test_argmax_ndarray():
    assert argmax(np.array([[1, 2], [3, 4]])) == 3


def test_abs():
    try:
        abs('1')
    except Exception as e:
        assert isinstance(e, TypeError)


def test_abs_ndarray():
    assert all_close(abs(np.array([[-1, -2], [-3, 4]])), [[1, 2], [3, 4]])


def test_unit():
    try:
        unit('1')
    except Exception as e:
        assert isinstance(e, TypeError)


def test_unit_ndarry():
    assert all_close(unit(np.array([1, 0])), np.array([1, 0], dtype=np.float))


def test_as_scalar():
    try:
        as_scalar('1')
    except Exception as e:
        assert isinstance(e, TypeError)


def test_as_scalar_ndarray_bool():
    assert as_scalar(np.array([22])) == 22
    assert as_scalar(np.bool_(False)) == False
    assert as_scalar(np.bool_(True)) == True


def test_square():
    try:
        square('1')
    except Exception as e:
        assert isinstance(e, TypeError)


def test_square_ndarry():
    assert all_close(square(np.array([-1j, 1])), [-1. + 0.j, 1. + 0.j])


def test_as_scalar_int_float_int32_int64_float32_float64_bool():
    assert as_scalar(1) == 1
    assert as_scalar(1.0) == 1
    assert as_scalar(np.int32(1)) == np.int32(1)
    assert as_scalar(np.int64(1)) == np.int64(1)
    assert as_scalar(np.float32(1.0)) == np.float32(1.0)
    assert as_scalar(np.float64(1.0)) == np.float64(1.0)
    assert as_scalar(False) == False
