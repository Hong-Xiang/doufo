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
    if xs is not None:
        if all(map(lambda a: isinstance(a, tf.Tensor), xs)):
            return tf.concat(xs.unbox(), axis=axis)
        if all(map(lambda a: isinstance(a, np.ndarray), xs)):
            return np.concatenate(xs.unbox(), axis=axis)
        else:
            res = List()
            for item in xs:
                res = res.extend(item)
            return res
