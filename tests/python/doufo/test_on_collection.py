from doufo import head, tail, take, List, flatten, concat
import pytest


@pytest.mark.parametrize('xs,expect', [
    ([1, 2, 3], [2, 3]),
    (List([1, 2, 3]), List([2, 3]))
])
def test_tail(xs, expect):
    assert tail(xs) == expect


@pytest.mark.parametrize('xs,expect', [
    ([1, 2, 3], 1),
    (List([1, 2, 3]), 1)
])
def test_head(xs, expect):
    assert head(xs) == expect


@pytest.mark.parametrize('xs,expect', [
    ((1, 2, 3), (1, 2, 3)),
    ((1, (2, 3)), (1, 2, 3)),
    ([1, [3, 4]], [1, 3, 4]),
    ([1,2], [1,2]),
    ((2,3), (2,3)),
])
def test_flatten(xs, expect):
    assert flatten(xs) == expect


@pytest.mark.parametrize('xs,expect', [
    ([[1], [2], [3]], [1, 2, 3]),
])
def test_concat(xs, expect):
    assert concat(xs, None) == expect
