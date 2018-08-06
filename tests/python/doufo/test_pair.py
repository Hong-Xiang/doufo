from doufo import Pair, dataclass, DataClass
import pytest


@pytest.mark.skip("not implemented yet.")
def test_generic():
    p = Pair[int, int](1, 2)


def test_eq():
    assert Pair(1, 2) == Pair(1, 2)


def test_neq():
    assert not Pair(1, 2) == Pair(1, 3)


def test_fmap():
    assert Pair(1, 2).fmap(lambda x, y: (x + 10, y + 10)) == Pair(11, 12)


def test_fmap2():
    assert Pair(1, 2).fmap2(lambda x: x + 1) == Pair(2, 3)


def test_flip():
    assert Pair(1, 2).flip() == Pair(2, 1)


def test_unbox():
    assert Pair(1, 2).unbox() == (1, 2)

def test_netsted():
    @dataclass
    class Point:
        x: float
        y: float
    
    @dataclass
    class Event(Pair):
        fst: Point
        snd: Point
    
    e = Event(Point(0.0, 1.0), Point(1.0, 2.0))
    assert issubclass(e.fields()['fst'].type, DataClass)