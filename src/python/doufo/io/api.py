from doufo import singledispatch
from typing import Type, Optional
import numpy as np
import pathlib
jfs = pathlib
from jfs import Path

__all__ = ['save', 'load', 'DataClassHints']


@singledispatch()
def save(data, path, xpath, slice_):
    pass


@singledispatch()
def load(data_class, path: Path, xpath: Optional[Path], slice_):
    pass


@load.register(Type[None])
def _(data_class, path: Path):
    data_class = guess_data_class(path.suffix)
    if data_class is None:
        raise TypeError
    return load(data_class, path)


class DataClassHints:
    hints = {}

    @classmethod
    def register(cls, key, data_class):
        cls.hints[key] = data_class

    @classmethod
    def find(cls, key):
        return cls.hints.get(key)


def guess_data_class(key):
    return DataClassHints.find(key)


@save.register(np.ndarray)
def save(data, path, xpath, slice_):
    if slice_ is not None:
        data = data[slice_]
    if xpath is None:
        np.save(path, data)
    else:
        np.savez(path, **{xpath: data})

