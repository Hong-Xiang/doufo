from dxl.data import Functor
from collections.abc import Iterable
from abc import abstractproperty, ABC
import numpy as np
from typing import TypeVar
import functools
import operator

from doufo.tensor import (to_tensor_like, as_scalar,
                          is_scalar, shape, ndim, as_scalar)
from .changeshape import 

T = TypeVar('TensorLike')


class Tensor(Functor[T]):
    # HACK for radd to work
    __array_priority__ = 16

    def __init__(self, data):
        from dxl.function.tensor import to_tensor_like
        self.data = to_tensor_like(data)

    def unbox(self):
        """
        Return un-wrapped raw tensor.
        """
        return self.data

    @property
    def shape(self):
        return shape(self.data)

    @property
    def ndim(self):
        return ndim(self.data)

    @property
    def size(self):
        return functools.reduce(operator.mul, self.shape, 1)

    def __getitem__(self, s):
        result = self.fmap(lambda d: d[s])
        # HACK unbox scalar
        return result if not is_result_scalar(result, s) else as_scalar(result)

    def __setitem__(self, s, v):
        def _assign(t):
            t[s] = v
            return t
        return self.fmap(_assign)

    def __iter__(self):
        return (Tensor(x) if not is_scalar(x) else as_scalar(x) for x in self.unbox())

    def fmap(self, f):
        return Tensor(f(self.unbox))

    def __eq__(self, t):
        return self.fmap(lambda d: d == t)

    def __req__(self, t):
        return self.fmap(lambda d: t == d)

    def __mul__(self, t):
        return self.fmap(lambda d: d * t)

    def __rmul__(self, t):
        return self.fmap(lambda d: t * d)

    def __matmul__(self, t):
        if isinstance(t, Tensor):
            t = t.join()
        return Tensor(self.join() @ t)

    def __rmatmaul__(self, t):
        if isinstance(t, Tensor):
            t = t.join()()
        return Tensor(t @ self.unbox())

    def __len__(self):
        return len(self.unbox())

    def __add__(self, t):
        return self.fmap(lambda d: d + t)

    def __radd__(self, t):
        return self.fmap(lambda d: t + d)

    def __sub__(self, t):
        return self.fmap(lambda d: d - t)

    def __rsub__(self, t):
        return self.fmap(lambda d: t - d)

    def __truediv__(self, t):
        return self.fmap(lambda d: d / t)

    def __rtruediv__(self, t):
        return self.fmap(lambda d: t / d)

    def __floordiv__(self, t):
        return self.fmap(lambda d: d // t)

    def __floordiv__(self, t):
        return self.fmap(lambda d: t // d)

    def __mod__(self, t):
        return self.fmap(lambda d: d % t)

    def __rmod__(self, t):
        return self.fmap(lambda d: t % d)

    def __neg__(self):
        return self.fmap(lambda d: -d)

    def __repr__(self):
        return repr(self.unbox)

    def __str__(self):
        return str(self.unbox)


def is_result_scalar(result, s):
    if result.ndim == 0 or isinstance(s, int):
        return True
    if isinstance(s, tuple) and all(map(lambda x: isinstance(x, int), s)):
        return True
    return False


__fmaped_funcs = [_square, _unit, _abs_]
__unboxed_funcs = [_as_scalar, _to_tensor_like, _is_scalar]

for f in __fmaped_funcs:
    f.register(Tensor)(lambda t: t.fmap(f))

for f in __unboxed_funcs:
    f.register(Tennsor)(lambda t: f(t.unbox()))


@transpose.register(Tensor)
def _(t, perm=None):
    return t.fmap(lambda t: transpose(t, perm))


@all_
