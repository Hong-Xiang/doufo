import tensorflow as tf

from doufo.tensor import split, shape


@split.register(tf.Tensor)
def _(t, nb_partition, id_partition, axis=0):
    with tf.variable_scope('split_with_index'):
        return tf.slice(t, split_start(shape(t), nb_partition, id_partition, axis),
                        split_shape(shape(t), nb_partition, id_partition, axis))


def split_start(shape, nb_partition, id_partition, axis):
    result = [0 for _ in range(len(shape))]
    result[axis] = id_partition * shape[axis] // nb_partition
    return result


def split_shape(shape, nb_partition, id_partition, axis):
    result = list(shape)
    result[axis] = shape[axis] // nb_partition
    return result


