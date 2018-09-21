from typing import Sequence, TypeVar

import numpy as np

from doufo import Functor, List, IterableElemMap, identity, head, concat, DataClass, flatten, converters

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

    def fmap(self, f) -> 'DataList[T]':
        result = [f(x) for x in self.unbox()]
        if len(result) == 0:
            return DataList([], None)
        return DataList(result, type(result[0]))

    def filter(self, f):
        return DataList([x for x in self.unbox() if f(x)], self.dataclass)


class DataArray(Sequence[T], Functor[T]):
    def __init__(self, data, dataclass, constructor=None):
        if isinstance(data, DataArray):
            self.data = data.data
        else:
            self.data = maybe_fill(data, dataclass)
            self.data = maybe_add_dtype(self.data, dataclass)
        self.dataclass = dataclass
        if constructor is None:
            constructor = numpy_structure_of_array_to_dataclass
        self.constructor = constructor

    def fmap(self, f):
        result = f(self.unbox())
        if isinstance(result, DataClass):
            return DataArray(result, type(result))
        from doufo.tensor import Tensor
        return Tensor(result)

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
            return self.constructor(self.data[s].view(np.recarray), self.dataclass)
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
    return concat([dtype_parse_item(k, v, root + k, dataclass_type)
                   for k, v in dataclass_type.fields().items()],
                  None)


def dtype_names(dataclass_type):
    return dtype_of(dataclass_type).names


def dtype_parse_item(k, v, name, dataclass_type):
    if not issubclass(v.type, DataClass):
        return [(name, v.type)]
    if isinstance(dataclass_type, type):
        to_parse = v.type
    else:
        to_parse = getattr(dataclass_type, k)
    return dtype_kernel(to_parse, name + '/')


@converters.register(DataList, DataArray)
def list_of_dataclass_to_numpy_structure_of_array(datas: DataList) -> DataArray:
    return DataArray(np.rec.array(list(datas.fmap(lambda c: flatten(c.as_nested_tuple()))),
                                  dtype_of(datas[0])),
                     datas.dataclass)


# TODO rename numpy_structure_of_array_to_dataclass to numpy_array_to_data_class


def numpy_structure_of_array_to_dataclass(data, dataclass):
    if isinstance(data, np.recarray):
        return from_numpy_structure_of_array(data, dataclass)
    if (isinstance(data, np.ndarray)
            and data.dtype.fields is None
            and not isinstance(data, np.recarray)):
        return from_normal_ndarray(data, dataclass)
    return from_numpy_structure_of_array(data, dataclass)


@converters.register(DataArray, DataList)
def data_array_to_data_list(datas):
    return DataList([x for x in datas], datas.dataclass)


def from_normal_ndarray(data, dataclass):
    return dataclass(*make_data_columns(data, dataclass))


def make_data_columns(data, dataclass):
    result = []
    for i, k in enumerate(dataclass.fields()):
        if i < data.shape[1]:
            result.append(data[:, i])
        else:
            result.append(np.full([data.shape[0]],
                                  dataclass.fields()[k].default,
                                  dataclass.fields()[k].type))
    return result


def from_numpy_structure_of_array(data, dataclass):
    return dataclass(*(data[k] for k in dataclass.fields()))


def maybe_fill(data, dataclass):
    if is_need_fill(data, dataclass):
        columns = make_data_columns(data, dataclass)
        return stack_columns(columns, dataclass)
    return data


def maybe_add_dtype(data, dataclass):
    if isinstance(data, np.recarray):
        return data
    if isinstance(data, np.ndarray) and data.dtype.fields is not None:
        return data
    return stack_columns([data[:, i] for i in range(data.shape[1])], dataclass)


def is_need_fill(data, dataclass):
    if isinstance(data, np.recarray):
        return False
    if (isinstance(data, np.ndarray) and data.dtype.fields is None):
        if len(data.shape) == 1:
            return len(dataclass.fields()) > 1

        if data.shape[1] < len(dataclass.fields()):
            return True
    return False


def stack_columns(columns, dataclass):
    result = np.zeros([columns[0].shape[0]], dtype_of(dataclass))
    for i, k in enumerate(dtype_names(dataclass)):
        result[k] = columns[i]
    return result
