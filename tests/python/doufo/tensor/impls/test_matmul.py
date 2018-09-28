from doufo.tensor import Vector, Tensor, matmul, Matrix
import numpy as np
import pytest


def test_Vector_Vector():
    v1 = Vector([[1, 2, 3], [4, 5, 6]])
    v2 = Vector([[1, 4], [2, 5], [3, 6]])

    assert matmul(v1, v2) == Vector([[14, 32], [32, 27]])


def test_Vector_ndarray():
    v = Vector([[1, 2, 3], [4, 5, 6]])
    n = np.array([[1, 4], [2, 5], [3, 6]])

    assert matmul(v, n) == Vector([[14, 32], [32, 27]])

    v = Vector([1, 4])
    n = np.array([1, 4])

    assert matmul(v, n) == np.array([17])


def test_Matrix_Vector():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    v = Vector([[1, 4], [2, 5], [3, 6]])

    assert matmul(m, v) == Vector([[14, 32], [32, 27]])


def test_Vector_Matrix():
    v = Vector([[1, 4], [2, 5], [3, 6]])
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert matmul(v, m) == Vector([[17, 22, 27], [22, 29, 36], [27, 36, 45]])


def test_Matrix_Matrix():
    m1 = Matrix([[1, 4], [2, 5], [3, 6]])
    m2 = Matrix([[1, 2, 3], [4, 5, 6]])

    assert matmul(m1, m2) == Matrix([[17, 22, 27], [22, 29, 36], [27, 36, 45]])


def test_Tensor_Tensor():
    t1 = Tensor([[1, 4], [2, 5], [3, 6]])
    t2 = Tensor([[1, 2, 3], [4, 5, 6]])

    assert matmul(t1, t2) == Tensor([[17, 22, 27], [22, 29, 36], [27, 36, 45]])


def test_Tensor_ndarray():
    t = Tensor([[1, 4], [2, 5], [3, 6]])
    n = np.array([[1, 2, 3], [4, 5, 6]])
    assert matmul(t, n) == Tensor([[17, 22, 27], [22, 29, 36], [27, 36, 45]])


def test_ndarray_Tensor():
    n = np.array([[1, 2, 3], [4, 5, 6]])
    t = Tensor([[1, 4], [2, 5], [3, 6]])
    assert matmul(n, t) == Tensor([[14, 32], [32, 27]])


# TODO
def test_Vector_Vector_ndarray():
    pass
