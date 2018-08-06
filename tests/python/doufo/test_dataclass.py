from doufo import dataclass


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
