import tensorflow as tf
import numpy as np
from doufo.tensor.backends import *


def test_import_backend():
    import doufo.tensor.backends
    assert "backend" in doufo.tensor.backends.__all__


def test_backend_Tensor():
    t = tf.constant([[1, 2], [3, 4]])
    assert backend(t) == TensorFlowBackend


def test_backend_ndarray():
    n = np.array([1.0, 1.0])
    assert backend(n) == NumpyBackend
