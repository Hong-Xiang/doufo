import numpy as np
from doufo.tensor import matmul, Matrix, Vector, Tensor, ndim

__all__ = []

@matmul.register(Vector)
def _(x, y):
    y = unfied_type(y)
    if isinstance(y, Vector):
        return vec_vec(x, y)
    if isinstance(y, Matrix):
        return vec_mat(x, y) 
    return ten_ten(x, y)

   
@matmul.register(Matrix)
def _(x, y):
    y = unfied_type(y)
    if isinstance(y, Vector):
        return mat_vec(x, y)
    if isinstance(y, Matrix):
        return mat_mat(x, y) 
    return ten_ten(x, y)

@matmul.register(Tensor)
def _(x, y):
    x = unfied_type(x)
    if isinstance(x, Tensor):
        return ten_ten(x, Tensor(y))
    return matmul(x, y)

@matmul.register(np.ndarray)
def _(x, y):
    return matmul(Tensor(x), y)

def unfied_type(t):
    if ndim(t) == 1:
        return Vector(t)
    if ndim(t) == 2:
        return Matrix(t)
    return Tensor(t)

def vec_vec(x, y):
    return x.unbox() @ y.unbox()

def vec_mat(x, y):
    return Vector(x.unbox() @ y.unbox())

def mat_vec(x, y):
    return Vector(x.unbox() @ y.unbox())

def mat_mat(x, y):
    return Matrix(x.unbox() @ y.unbox())

def ten_ten(x, y):
    return Tensor(x.unbox() @ y.unbox())