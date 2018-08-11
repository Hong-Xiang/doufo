from doufo import dataclass, replace, Pair, convert_to
from doufo.collections import DataList, DataArray, list_of_dataclass_to_numpy_structure_of_array
from doufo.collections.dataclasses_ import dtype_kernel, make_data_columns, stack_columns
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
    soa.filter(lambda c: c.a >= 3)
    soa.fmap(lambda c: c.a)


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


def test_construct_data_array_from_normal_numpy_array():
    @dataclass
    class Point:
        x: float
        y: float

    data = np.ones([10, 2], np.float32)
    ds = DataArray(data, Point)
    assert len(ds) == 10
    assert ds[0] == Point(1.0, 1.0)


def test_construct_data_array_from_normal_numpy_array_with_defaults():
    @dataclass
    class Point:
        x: float
        y: float = 3.0

    data = np.ones([10, 1], np.float32)
    ds = DataArray(data, Point)
    assert len(ds) == 10
    assert ds[0] == Point(1.0, 3.0)


def test_make_data_columns():
    @dataclass
    class Point:
        x: float
        y: float = 3.0

    data = np.ones([10, 1], np.float32)
    result = make_data_columns(data, Point)
    assert len(result) == 2
    assert result[0].shape == (10,)
    assert result[1].shape == (10,)
    assert result[0][0] == 1.0
    assert result[1][0] == 3.0


def test_stack_columns():
    @dataclass
    class Point:
        x: float
        y: float
    data = [np.ones([10], float), np.ones([10], float)]
    result = stack_columns(data, Point)
    assert result.shape == (10,)
    assert result.dtype.fields is not None


def test_data_array_from_normal_array_for_nested_data_class():
    @dataclass
    class Point:
        x: float
        y: float

    @dataclass
    class Event(Pair):
        fst: Point
        snd: Point

    data = np.ones([10, 4])

    def constructor(data, dataclass):
        return Event(Point(data['fst/x'], data['fst/y']),
                     Point(data['snd/x'], data['snd/y']))
    da = DataArray(data, Event, constructor)
    assert da.shape[0] == 10
    assert da[0].fst.x == 1.0


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


def test_convert_from_data_list_to_data_array():
    @dataclass
    class Point:
        x: float
        y: float

    dl = DataList([Point(0.0, 0.0) for _ in range(10)])
    da = convert_to(dl, DataArray)
    assert len(dl) == 10
    assert all(map(lambda x: isinstance(x, Point), dl))
