from functools import singledispatch
from dxl.data import Monoid

__all__ = ['concat']


@singledispatch
def concat(xs):
    raise TypeError


@concat.register(Monoid)
def _(xs):
    return type(xs).concat(xs)
