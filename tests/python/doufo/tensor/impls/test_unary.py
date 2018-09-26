import tensorflow as tf
from doufo.tensor.impls.unary import *


def test_split_start():
    assert split_start([1, 2], 1, 1, 1) == [0, 2]


def test_split_shape():
    assert split_shape([1, 2], 1, 1, 1) == [1, 2]


def test_split():
    t = tf.constant([[1, 2], [3, 4]], dtype=tf.int64)
    result = split(t, 1, 1)
    assert str(result) == """Tensor("split_with_index/Slice:0", shape=(2, 2), dtype=int64)"""
