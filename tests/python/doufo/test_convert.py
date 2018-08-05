from doufo.convert import tuple_type_compare, single_type_compare
import pytest


class B0:
    pass


class D0(B0):
    pass


class C:
    pass


@pytest.mark.parametrize('t0,t1,expect', [
    ((B0, B0), (D0, D0), -1),
    ((D0, D0), (B0, B0), 1),
    ((D0, B0), (B0, D0), 1),
    ((D0, D0), (D0, B0), 1),
    ((D0, D0), (D0, D0), 0),
])
def test_tuple_type_comprae(t0, t1, expect):
    assert tuple_type_compare(t0, t1) == expect


@pytest.mark.parametrize('t0,t1,expect', [
    (D0, D0, 0),
    (B0, B0, 0),
    (D0, B0, 1),
    (B0, D0, -1),
    (C, D0, 0),
])
def test_single_type_compare(t0, t1, expect):
    assert single_type_compare(t0, t1) == expect
