from .tensor import Tensor
from typing import TypeVar
from .binary import matmul

T = TypeVar('T')

__all__ = ['Vector', 'project']


class Vector(Tensor[T]):
    def __init__(self, data):
        super().__init__(data)
        # if self.ndim > 1:
        # raise ValueError(f"Vector must be 1 dimensional or scalar, got {self.ndim}.")

    def fmap(self, f):
        return Vector(f(self.data))

    # def __matmul__(self, t):
    #     return matmul(self, t)
    #     from .matrix import Matrix
    #     from dxl.function.tensor import transpose
    #     # HACK for v @ t.T
    #     if len(t.shape) == 2 and t.shape[0] == 1 and t.shape[1] == self.size:
    #         return self @ transpose(t)
    #     return scalar_or_vector_of(Tensor(self) @ Tensor(t), t)

    # def __rmatmul__(self, t):
    #     from .matrix import Matrix
    #     return scalar_or_vector_of(Tensor(t) @ Tensor(self), t)

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @classmethod
    def one_hot(cls, n, l):
        """
        n: position of "hot"
        l: lenght of vector
        """
        v = [0.0 for _ in range(l)]
        v[n] = 1.0
        return Vector(v)


def scalar_or_vector_of(result, t):
    from dxl.function.tensor import as_scalar
    return as_scalar(result) if is_result_scalar(t) else Vector(result)


def is_result_scalar(t):
    return isinstance(t, Vector)


def project(v: Vector, n: Vector) -> Vector:
    """
    Project Vector v onto plane with normal vector n.
    """
    v, n = Vector(v), Vector(n)
    return v - v @ n * n / (n @ n)
