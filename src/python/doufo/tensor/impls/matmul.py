import numpy as np
from doufo.tensor import matmul, Matrix, Vector, Tensor, ndim, as_scalar, project

__all__ = []


@matmul.register(Vector, Vector)
def _(x, y):
    return x.unbox() @ y.unbox()


@matmul.register(Vector, np.ndarray)
def _(x, y):
    if y.ndim <= 1:
        return x.unbox() @ y
    return x.fmap(lambda _: matmul(_, y))


@matmul.register(Matrix, Vector)
def _(x, y):
    return y.fmap(lambda _: matmul(x.unbox(), _))


@matmul.register(Vector, Matrix)
def _(x, y):
    return x.fmap(lambda _: _ @ y.unbox())


@matmul.register(Matrix, Matrix)
def _(x, y):
    return x.fmap(lambda _: _ @ y.unbox())


@matmul.register(Tensor, Tensor)
def _(x, y):
    return x.fmap(lambda _: _ @ y.unbox())


@matmul.register(Tensor, np.ndarray)
def _(x, y):
    return x.fmap(lambda _: matmul(_, y))


@matmul.register(np.ndarray, Tensor)
def _(x, y):
    return y.fmap(lambda _: matmul(x, _))


@project.register(Vector, (Vector, np.ndarray))
def _(v, n):
    return v.fmap(lambda _: project(_, n))


