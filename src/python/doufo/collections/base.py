import collections.abc
from typing import Generic, TypeVar
from dxl.data import Functor, Monoid
import types

a = TypeVar('a')

from enum import Enum


class Iterable(collections.abc.Iterable[a], Functor[a], Monoid[a]):
    pass


class Collection(Iterable[a], collections.abc.Collection[a]):
    pass


