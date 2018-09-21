from doufo import Functor
from typing import TypeVar
import functools
import operator
from doufo import FunctorArithmeticMixin
from .binary import *
from .unary import *
from .unary_reduce import *
from .unary_with_args import *

from doufo.tensor import to_tensor_like, as_scalar, is_scalar, shape, ndim, sum_, shape, argmax, matmul

T = TypeVar('T')  # TensorLike

__all__ = ['Tensor']

class Tensor(Functor[T], FunctorArithmeticMixin):
    # HACK for radd to work
    __array_priority__ = 16

    def __init__(self, data):
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
        self.unbox()[s] = v

    def __iter__(self):
        return (Tensor(x) if not is_scalar(x) else as_scalar(x) for x in self.unbox())

    def fmap(self, f):
        return Tensor(f(self.unbox()))

    def __matmul__(self, t):
        return matmul(self, t)

    def __rmatmaul__(self, t):
        return matmul(t, self)

    def __len__(self):
        return len(self.unbox())

    def __repr__(self):
        return repr(self.unbox())

    def __str__(self):
        return str(self.unbox())


def is_result_scalar(result, s):
    if result.ndim == 0 or isinstance(s, int):
        return True
    if isinstance(s, tuple) and all(map(lambda x: isinstance(x, int), s)):
        return True
    return False


@square.register(Tensor)
def _(t):
    return t.fmap(square)


@unit.register(Tensor)
def _(t):
    return t.fmap(unit)


@abs_.register(Tensor)
def _(t):
    return t.fmap(abs_)


@as_scalar.register(Tensor)
def _(t):
    return as_scalar(t.unbox())


@to_tensor_like.register(Tensor)
def _(t):
    return to_tensor_like(t.unbox())


@is_scalar.register(Tensor)
def _(t):
    return is_scalar(t.unbox())


@sum_.register(Tensor)
def _(t):
    return sum_(t.unbox())


@ndim.register(Tensor)
def _(t):
    return ndim(t.unbox())


@transpose.register(Tensor)
def _(t, perm=None):
    return t.fmap(lambda t: transpose(t, perm))


@norm.register(Tensor)
def _(t, p=2.0):
    return norm(t.unbox(), p)


@all_close.register(Tensor)
def _(x, y):
    return all_close(x.unbox(), Tensor(y).unbox())


@shape.register(Tensor)
def _(t):
    return shape(t.unbox())


@argmax.register(Tensor)
def _(t):
    return argmax(t.unbox())


@flatten.register(Tensor)
def _(x, batch_dim=0):
    return x.fmap(lambda _: flatten(_, batch_dim))


@matmul.register(Tensor, Tensor)
def _(x, y):
    return x.fmap(lambda _: matmul(_, y.unbox()))
