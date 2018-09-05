from functools import singledispatch
from doufo import Monoid, List
import numpy as np
import tensorflow as tf

__all__ = ['concat']


@singledispatch
def concat(xs, axis=0):
    raise TypeError


@concat.register(Monoid)
def _(xs, axis=0):
    return type(xs).concat(xs)


@concat.register(List)
def _(xs, axis=0):
    if type(xs) != List:
        raise ValueError('xs must be doufo.list.List obj.')
    if type(xs[0]) == tf.Tensor:
        return tf.concat(xs.unbox(), axis=axis)
    if type(xs[0]) == np.ndarray:
        return np.concatenate(xs.unbox(), axis=axis)
    else:
        res = List()
        for item in xs:
            res = res.extend(item)
        return res
