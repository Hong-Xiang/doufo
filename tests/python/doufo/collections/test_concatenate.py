from doufo.collections.concatenate import concat
import tensorflow as tf
import numpy as np
from doufo.list import List
from doufo.tensor.binary import all_close


def test_List_concatenate_with_tf_tensor():
    b = tf.constant([[1, 2], [3, 4]])
    c = tf.constant([[5, 6], [7, 8]])
    q = tf.concat([b, c], axis=1)
    d = concat(List([b, c]), axis=1)
    with tf.Session() as sess:
        res1, res2 = sess.run([d, q])
    assert all_close(res1, res2) is True


def test_List_concatenate_with_np_array():
    e = np.array([[1, 2], [3, 4]])
    f = np.array([[5, 6], [7, 8]])
    w = concat(List([e, f]), axis=1)
    q = np.array([[1, 2, 5, 6], [3, 4, 7, 8]])
    assert all_close(w, q) is True


def test_List_concatenate_basic():
    a = List([[1], [2], [3]])
    a = concat(a)
    assert a == [1, 2, 3]
