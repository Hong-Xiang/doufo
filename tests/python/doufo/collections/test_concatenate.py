from doufo.collections.concatenate import concat
import tensorflow as tf
import numpy as np
from doufo.list import List


def test_List_concatenate():
    a = List([[1], [2], [3]])
    b = tf.constant([[1, 2], [3, 4]])
    c = tf.constant([[5, 6], [7, 8]])
    e = np.array([[1, 2], [3, 4]])
    f = np.array([[5, 6], [7, 8]])
    q = tf.concat([b, c], axis=1)
    d = concat(List([b, c]), axis=1)
    w = concat(List([e, f]), axis=1)
    a = concat(a)
    with tf.Session() as sess:
        res1, res2 = sess.run([d, q])
    assert res1.all() == res2.all()
    assert w.all() == np.array([[1, 2, 5, 6], [3, 4, 7, 8]]).all()
    assert a == [1, 2, 3]
