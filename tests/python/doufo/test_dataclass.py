import attr
from attr.exceptions import FrozenInstanceError

from doufo import dataclass, DataClass, replace, fields


def test_as_tuple():
    @dataclass
    class Point:
        x: float
        y: float
    p = Point(1.0, 2.0)
    assert p.as_tuple() == (1.0, 2.0)


def test_as_nested_tuple():
    @dataclass
    class Point:
        x: float
        y: float

    @dataclass
    class Event:
        fst: Point
        snd: Point

    e = Event(Point(1.0, 2.0), Point(3.0, 4.0))
    assert e.as_nested_tuple() == ((1.0, 2.0), (3.0, 4.0))

def test_as_dict():
    @dataclass
    class Point:
        x: float
        y: float

    p = Point(1.0, 2.0)
    assert p.as_dict() == {'x': 1.0, 'y': 2.0}

def test_fields():
    @attr.s
    class C(DataClass):
        x = attr.ib()
        y = attr.ib()

    assert C.fields()['x'] is attr.fields(C).x
    assert C.fields()['y'] is attr.fields(C).y

def test_replace():
    @attr.s
    class C(DataClass):
        x = attr.ib()
        y = attr.ib()

    i1 = C(1, 2)
    i2 = i1.replace(y=3)
    assert i2.x == 1
    assert i1 != i2


def test_dataclass():
    class A():
        x: float
        y: float

    B = dataclass(A)
    b = B(1.0, 2.0)
    assert b.as_dict() == {'x': 1.0, 'y': 2.0}

    try:
        b.x = 2
    except Exception as e:
        assert isinstance(e,FrozenInstanceError)

def test_skin_replace():
    @attr.s
    class C(DataClass):
        x = attr.ib()
        y = attr.ib()

    i1 = C(1, 2)

    i2 = replace(i1, y=3)
    assert i2.x == 1
    assert i1 != i2

def test_skin_fields():
    @attr.s
    class C(DataClass):
        x = attr.ib()
        y = attr.ib()
    assert fields(C)['x'] is attr.fields(C).x
    assert fields(C)['y'] is attr.fields(C).y