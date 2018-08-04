import collections.abc
from typing import Sequence, TypeVar
import numpy as np
from doufo import Functor, Monad,List, IterableElemMap, IterableIterMap
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
        return DataList(result, type(result))

    def filter(self, f):
        return DataList([x for x in self.unbox() if f(x)], self.dataclass)


class DataArray(Sequence[T], Functor[T]):
    def __init__(self, data, dataclass, constructor=None):
        self.data = data
        self.dataclass = dataclass
        from dxl.function.collections.dataclass import numpy_structure_of_array_to_dataclass
        if constructor is None:
            constructor = numpy_structure_of_array_to_dataclass
        self.constructor = constructor

    def fmap(self, f):
        result = self.unbox()
        return DataArray(type(result), f(result))

    def __len__(self):
        return self.data.shape[0]

    def filter(self, f):
        result = self.data[f(self.unbox())]
        return DataArray(result, self.dataclass)

    def __getitem__(self, s):
        if isinstance(s, int):
            return self.unbox()[s]
        else:
            return self.fmap(lambda d: d[s])

    def unbox(self):
        return self.constructor(self.data.view(np.recarray), self.dataclass)

    def __repr__(self):
        return f"<DataArray({self.dataclass}, {self.unbox()})>"




class DataIterable(IterableElemMap):
    def __init__(self, data, dataclass=None):
        from dxl.function import head
        self.data = data
        if dataclass is None:
            dataclass = type(head(data))
        self.dataclass = dataclass

    def unbox(self):
        return self.data

    def fmap(self, f):
        from dxl.function import head
        result = f(head(self.join()))
        return DataIterable(self.data.fmap(f), type(result))

    def filter(self, f):
        return DataIterable(IterableIterMap(self, partial(filter, f)))

__all__ += ['list_of_dataclass_to_numpy_structure_of_array']

def dtype_of(dataclass_type):
    return np.dtype([(k, v.type) for k, v in dataclass_type.fields().items()], align=True)

def list_of_dataclass_to_numpy_structure_of_array(datas,):
    return np.rec.array(list(datas.fmap(lambda c: c.as_tuple())), dtype_of(datas[0]))

def numpy_structure_of_array_to_dataclass(data, dataclass):
    return dataclass(*(data[k] for k in dataclass.fields()))
