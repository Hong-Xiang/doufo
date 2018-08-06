import collections.abc
from typing import Sequence, TypeVar
import numpy as np
from doufo import (Functor, Monad, List, IterableElemMap, IterableIterMap,
                   Monoid, identity, head, concat, DataClass, flatten,
                   converters, convert_to)
from functools import partial

__all__ = ['DataList', 'DataArray', 'DataIterable']


def batched(f):
    return f


T = TypeVar('T')


class DataList(List[T]):
    def __init__(self, data, dataclass=None):
        super().__init__(data)
        if dataclass is None:
            dataclass = type(data[0])
        self.dataclass = dataclass

    def fmap(self, f):
        result = [f(x) for x in self.unbox()]
        if len(result) == 0:
            return DataList([], None)
        return DataList(result, type(result))

    def filter(self, f):
        return DataList([x for x in self.unbox() if f(x)], self.dataclass)


class DataArray(Sequence[T], Functor[T]):
    def __init__(self, data, dataclass, constructor=None):
        self.data = data
        self.dataclass = dataclass
        if constructor is None:
            constructor = numpy_structure_of_array_to_dataclass
        self.constructor = constructor

    def fmap(self, f):
        result = self.unbox()
        return DataArray(type(result), f(result))

    def __len__(self):
        # return self.unbox().shape[0]
        return self.shape[0]
    
    @property
    def shape(self):
        return self.data.shape

    def filter(self, f):
        result = self.data[f(self.unbox())]
        return DataArray(result, self.dataclass)

    def __getitem__(self, s):
        if isinstance(s, int):
            return self.unbox()[s]
        else:
            return DataArray(self.data[s], self.dataclass)

    def unbox(self):
        return self.constructor(self.data.view(np.recarray), self.dataclass)

    def __repr__(self):
        return f"<DataArray({self.dataclass}, {self.unbox()})>"

    def extend(self, xs: 'DataArray[T]') -> 'DataArray[T]':
        if len(xs) == 0:
            return self
        if len(self) == 0:
            return xs
        return self.fmap(lambda d: np.concatenate([d, xs.unbox()]))

    @classmethod
    def empty(cls):
        return DataArray(np.array([]), None, identity)


class DataIterable(IterableElemMap):
    def __init__(self, data, dataclass=None):
        super().__init__(data)
        if dataclass is None:
            dataclass = type(head(data))
        self.dataclass = dataclass

    def fmap(self, f):
        result = f(head(self.unbox()))
        return DataIterable(self, type(result))

    def filter(self, f):
        return DataIterable(super().filter(f), self.dataclass)


__all__ += ['list_of_dataclass_to_numpy_structure_of_array']


def dtype_of(dataclass_type):
    return np.dtype(dtype_kernel(dataclass_type, ''), align=True)


def dtype_kernel(dataclass_type, root):
    return concat([dtype_parse_item(k, v, root+k, dataclass_type)
                   for k, v in dataclass_type.fields().items()],
                  None)


def dtype_parse_item(k, v, name, dataclass_type):
    if not issubclass(v.type, DataClass):
        return [(name, v.type)]
    if isinstance(dataclass_type, type):
        to_parse = v.type
    else:
        to_parse = getattr(dataclass_type, k)
    return dtype_kernel(to_parse, name+'/')


@converters.register(DataList, DataArray)
def list_of_dataclass_to_numpy_structure_of_array(datas):
    return np.rec.array(list(datas.fmap(lambda c: flatten(c.as_nested_tuple()))),
                        dtype_of(datas[0]))


def numpy_structure_of_array_to_dataclass(data, dataclass):
    if data.dtype.fields is None:
        return from_normal_ndarray(data, dataclass)
    else:
        return from_numpy_structure_of_array(data, dataclass)


def from_normal_ndarray(data, dataclass):
    return dataclass(*(data[:, i] for i, _ in enumerate(dataclass.fields())))


def from_numpy_structure_of_array(data, dataclass):
    return dataclass(*(data[k] for k in dataclass.fields()))
