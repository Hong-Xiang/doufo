from doufo.tensor import Matrix, Vector, all_close
import numpy as np


def test_matmul_mv():
    result = Matrix([[1, 2], [3, 4], [5, 6]]) @ Vector([7, 8])
    assert isinstance(result, Vector)
    assert all_close(result, Vector([23, 53, 83]))


def test_matmul_vm():
    result = Vector([7, 8, 9]) @ Matrix([[1, 2], [3, 4], [5, 6]])
    assert isinstance(result, Vector)
    assert all_close(result, Vector([76, 100]))


def test_init():
    assert Matrix([[1, 2, 3], [4, 5, 6]]) == np.array([[1, 2, 3], [4, 5, 6]])


def test_fmap():
    def func(data):
        return data * 2

    assert Matrix([[1, 2, 3], [4, 5, 6]]).fmap(func) == np.array([[2, 4, 6], [8, 10, 12]])


def test_eye():
    res = Matrix.eye(3)

    assert res == np.eye(3)
    assert isinstance(res, Matrix)


def test_one_hot1():
    assert Matrix.one_hot([1, 2], [3, 4])==np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]], dtype=float)


def test_one_hot2():
    try:
        Matrix.one_hot([1, 2], [1, 2])
    except Exception as e:
        assert e is not None


def test_one_hot3():
    assert all_close(Matrix.one_hot(1, 3), np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=float))
