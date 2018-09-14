import pytest
import tensorflow as tf


@pytest.fixture()
def tf_test_session():
    with tf.Graph().as_default():
        with tf.Session() as sess:
            yield sess
