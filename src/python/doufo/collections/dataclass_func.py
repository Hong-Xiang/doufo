import numpy as np
from functools import singledispatch


def fields(dataclass_type):
    return dataclass_type.__slots__


def dtype_of(dataclass_type, type_hints=None):
    if type_hints is not None:
        dtypes = [(f, t) for f, t in zip(fields(dataclass_type), type_hints)]
    else:
        dtypes = [(f, v) for f, v in dataclass_type.fields().items()]
    return np.dtype(dtypes, align=True)


def list_of_dataclass_to_numpy_structure_of_array(datas, types=None):
    return np.rec.array(list(datas.fmap(lambda c: c.astuple())),
                        dtype_of(type(datas[0]), types))


def numpy_structure_of_array_to_dataclass(data, dataclass):
    return dataclass(*(data[k] for k in dataclass.fields()))
