from doufo import dataclass, replace, Pair, convert_to
from doufo.collections import DataList, DataArray, list_of_dataclass_to_numpy_structure_of_array
from doufo.collections.dataclasses_ import dtype_kernel
import operator
import numpy as np
import attr


def test_aos_soa_campat():
    @dataclass
    class C:
        a: int
        b: int
    aos = DataList([C(1, 2), C(3, 4), C(5, 6)])
    soa = DataArray(list_of_dataclass_to_numpy_structure_of_array(aos), C)
    aos.filter(lambda c: c.a >= 3)
    aos.fmap(lambda c: c.a)
    aos.fmap(lambda c: replace(c, a=c.a + 1))
    soa.filter(lambda c: c.a >= 3)
    soa.fmap(lambda c: c.a)
    soa.fmap(lambda c: replace(c, a=c.a + 1))


def test_dtype_kernel_single():
    @dataclass
    class Point:
        x: np.float
        y: np.float
    assert dtype_kernel(Point, '') == [('x', float), ('y', float)]


def test_dtype_kernel_nested():
    @dataclass
    class Point:
        x: np.float
        y: np.float

    @dataclass
    class Event(Pair):
        fst: Point
        snd: Point
    assert dtype_kernel(Event, '') == [('fst/x', float), ('fst/y', float),
                                       ('snd/x', float), ('snd/y', float)]


def test_dtype_kernel_nested_abstract():
    @dataclass
    class Point:
        pass

    @dataclass
    class PointC:
        x: float
        y: float

    @dataclass
    class PointR:
        r: float
        t: float

    @dataclass
    class Event(Pair):
        fst: Point
        snd: Point
    e = Event(PointC(0.0, 1.0), PointR(1.0, 3.0))
    assert dtype_kernel(e, '') == [('fst/x', float), ('fst/y', float),
                                   ('snd/r', float), ('snd/t', float)]

def test_construct_data_array_from_norma_numpy_array():
    @dataclass
    class Point:
        x: float
        y: float

    data = np.ones([10, 2], np.float32)
    ds = DataArray(data, Point)
    assert len(ds) == 10


def test_convert_from_data_array_to_data_list():
    @dataclass
    class Point:
        x: float
        y: float

    data = np.ones([10, 2], np.float32)
    ds = DataArray(data, Point)
    dl = convert_to(ds, DataList)
    assert len(dl) == 10
    assert all(map(lambda x: isinstance(x, Point), dl))


