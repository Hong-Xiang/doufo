from .tensor import Tensor
import numpy as np
# from doufo.tensor import ndim

__all__ = ["Matrix"]

class Matrix(Tensor):
    def __init__(self, data):
        super().__init__(data)
        # if self.ndim != 2:
        # raise ValueError(f"Vector must be 1 dimensional, got {self.ndim}.")

    def fmap(self, f):
        return Matrix(f(self.data))

    # def __matmul__(self, t):
        # result = Tensor(self) @ Tensor(t)
        # if isinstance(t, Vector):
        #     return Vector(result)
        # if isinstance(t, Matrix):
        #     return Matrix(result)
        # return Vector(result) if ndim(result) <= 1 else Matrix(result)

    # def __rmatmaul__(self, t):
    #     from .vector import Vector
    #     result = Tensor(t) @ Tensor(self)
    #     if isinstance(t, Vector):
    #         return Vector(result)
    #     return Matrix(result)

    # TODO improve impl of following methods

    @classmethod
    def eye(cls, n):
        return Matrix(np.eye(n))

    @classmethod
    def one_hot(cls, ij, sz):
        """
        ij: postion
        sz: size of matrix
        """
        if isinstance(sz, int):
            sz = (sz, sz)
        if isinstance(ij, int):
            ij = (ij, ij)
        m = np.zeros(sz)
        m[ij[0], ij[1]] = 1.0
        return Matrix(m)
