from doufo.tensor import Tensor
import numpy as np
from doufo.tensor.construct import *
from doufo.tensor import all_close


def test_import():
    import doufo.tensor.construct
    assert doufo.tensor.construct.__all__ == ['to_tensor_like', 'array', 'const', 'copy', 'sparse']


def test_to_tensor_like():
    assert all_close(to_tensor_like([1, 2]), np.array([1, 2]))


def test_to_tensor_like_ndarray():
    t = Tensor([[1, 4], [2, 5], [3, 6]])
    assert to_tensor_like(t) == Tensor([[1, 4], [2, 5], [3, 6]])


def test_to_tensor_like_Tensor():
    n = np.array([[1, 2, 3], [4, 5, 6]])
    assert all_close(to_tensor_like(n) == np.array([[1, 2, 3], [4, 5, 6]]))


def test_array():
    try:
        array((2,), dtype=np.int64)
    except Exception as e:
        assert isinstance(e, NotImplementedError)


def test_sparse():
    try:
        sparse([1])
    except Exception as e:
        assert isinstance(e, NotImplementedError)


def test_const():
    try:
        const([1])
    except Exception as e:
        assert isinstance(e, NotImplementedError)


def test_copy():
    try:
        copy([1])
    except Exception as e:
        assert isinstance(e, NotImplementedError)
