from functools import singledispatch
from doufo import Monoid

__all__ = ['concat']


@singledispatch
def concat(xs):
    raise TypeError


@concat.register(Monoid)
def _(xs):
    return type(xs).concat(xs)
