import collections.abc
from typing import Sequence, TypeVar

from doufo import Functor, Monad,List, IterableElemMap, IterableIterMap
from functools import partial
__all__ = ['DataList', 'DataArray', 'DataIterable']


def batched(f):
    return f


a = TypeVar('a')


class DataCollection(Sequence[a], Functor[a], Monoid[a]):
    pass


class DataList(DataCollection[a], List[a]):
    def __init__(self, data, dataclass=None):
        super().__init__(data)
        if dataclass is None:
            dataclass = type(data[0])
        self.dataclass = dataclass

    def fmap(self, f):
        result = [f(x) for x in self.join()]
        return DataList(result, type(result))

    def filter(self, f):
        return DataList([x for x in self.join() if f(x)], self.dataclass)


class DataArray(Sequence[a], Functor[a]):
    def __init__(self, data, dataclass, constructor=None):
        self.data = data
        self.dataclass = dataclass
        from dxl.function.collections.dataclass import numpy_structure_of_array_to_dataclass
        if constructor is None:
            constructor = numpy_structure_of_array_to_dataclass
        self.constructor = constructor

    def fmap(self, f):
        result = f((self.join()))
        return DataArray(type(result), result)

    def __len__(self):
        return self.data.shape[0]

    def filter(self, f):
        result = self.join()[f(self.join())]
        return DataArray(result, self.dataclass)

    def __getitem__(self, s):
        if isinstance(s, int):
            return self.join()[s]
        else:
            return self.fmap(lambda d: d[s])

    def join(self):
        view = np.arr.view(self.data, np.recarray)
        return self.constructor(view)

    def __repr__(self):
        return f"<DataArray({self.dataclass}, {self.join()})>"




class DataIterable(IterableElemMap):
    def __init__(self, data, dataclass=None):
        from dxl.function import head
        self.data = data
        if dataclass is None:
            dataclass = type(head(data))
        self.dataclass = dataclass

    def join(self):
        return self.data

    def fmap(self, f):
        from dxl.function import head
        result = f(head(self.join()))
        return DataIterable(self.data.fmap(f), type(result))

    def filter(self, f):
        return DataIterable(IterableIterMap(self, partial(filter, f)))
