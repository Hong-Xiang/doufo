from doufo.tensor import Tensor, all_close
import numpy as np
from doufo.tensor.unary import *
from doufo.tensor.construct import *
from doufo.tensor.unary_reduce import *
from doufo.tensor.unary_with_args import *
import tensorflow as tf


def test_add():
    a, b = Tensor([1, 2]), Tensor([3, 4])
    c = Tensor([4, 6])
    assert all_close(a + b, c)


def test_init():
    assert all_close(Tensor([1, 2]), [1, 2])


def test_unbox():
    assert all_close(Tensor([1, 2]).unbox(), [1, 2])


def test_shape():
    assert Tensor([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]]).shape == [2, 2, 3]


def test_ndim():
    assert Tensor([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]]).ndim == 3


def test_size():
    assert Tensor([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]]) == 12


# TODO
def test_getitem():
    pass


# TODO
def test_setitem():
    pass


def test_iter():
    t = Tensor([[1, 2], [3, 4]])
    t_iter = iter(t)
    assert next(t_iter) == [1, 2]
    assert next(t_iter) == [3, 4]


def test_fmap():
    t = Tensor([[1, 2], [3, 4]])

    def func(data):
        return data * 2

    assert all_close(t.fmap(func), [[2, 4], [6, 8]])


def test_matmul():
    t1 = Tensor([[1, 2], [1, 2]])
    t2 = Tensor([[1, 2], [1, 2]])

    assert all_close(t1 @ t2, [[3, 6], [3, 6]])


# TODO
def test_rmatmul():
    pass


def test_len():
    assert len(Tensor([1, 2, 3])) == 3


def test_repr():
    assert repr(Tensor([1, 2, 3])) == repr(np.array([1, 2, 3]))


def test_str():
    assert str(Tensor([1, 2, 3])) == str(np.array([1, 2, 3]))


import doufo.tensor


def test_is_result_scalar():
    assert doufo.tensor.tensor.is_result_scalar(np.array([1, 2]), 1) == True
    assert doufo.tensor.tensor.is_result_scalar(np.array([1, 2]), (1, 2)) == True
    assert doufo.tensor.tensor.is_result_scalar(np.array([1, 2]), [1]) == False


def test_square():
    assert all_close(square(Tensor([[1, 2], [3, 4]])), np.array([[1, 4], [9, 16]]))


def test_unit():
    assert all_close(unit(Tensor([0, 1])), np.array([0, 1], dtype=np.float64))


def tests_abs_():
    assert all_close(abs_(Tensor([[-1, -2], [-3, 4]])), [[1, 2], [3, 4]])


def test_as_scalar():
    assert as_scalar(Tensor([22])) == 22


def test_to_tensor_like():
    t = Tensor([[1, 2], [3, 4]])
    res_t = to_tensor_like(t)

    assert res_t == t


def test_is_scalar():
    assert is_scalar(Tensor([1, 2])) == False


def test_sum_():
    assert sum_(Tensor([[1, 2], [3, 4]])) == 10


def test_ndim_():
    assert ndim(Tensor([[1, 2], [3, 4]])) == 2


def test_transpose():
    with tf.Graph().as_default():
        t = Tensor([[1, 2, 3], [4, 5, 6]])
        assert transpose(t) == [[1, 4], [2, 5], [3, 6]]


def test_norm():
    t = Tensor([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    assert norm(t) == 7.745966692414834


def test_all_close():
    assert all_close(Tensor([1]), Tensor([1])) == True
    assert all_close(Tensor([1]), Tensor([2])) == False


def test_shape_Tensor():
    assert shape(Tensor([1])) == [1]
    assert shape(Tensor([[1], [1]])) == [2, 1]


def test_argmax():
    assert np.argmax(Tensor([[1, 2], [2, 7]])) == 3
    assert all_close(np.argmax(Tensor([[1, 2], [2, 7]]), axis=0), [1, 1])
    assert all_close(np.argmax(Tensor([[1, 2], [2, 7]]), axis=1), [1, 1])


def test_alatten():
    f1 = flatten(Tensor([1, 2, 3, 4]))
    assert f1.shape == [4, 1]
    assert f1.ndim == 2

    f2 = flatten(Tensor([[1, 2, 3], [3, 4, 5]]))
    assert f2.shape == [2, 3]
    assert f2.ndim == 2

    f3 = flatten(Tensor([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]]))
    assert f3.shape == [3, 6]
    assert f3.ndim == 2
#TODO(there are two @matmul.register(Tensor, Tensor) in project)
def test_matmul_Tensor_Tensor():
    pass