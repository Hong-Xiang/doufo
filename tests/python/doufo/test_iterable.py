import pytest
from functools import partial
from itertools import dropwhile
from doufo import IterableElemMap, IterableIterMap,Count
from doufo.on_collections import take_


def test_itertools_iterable():
    it = IterableIterMap(range(10), partial(dropwhile, lambda x: x < 3))
    assert list(it) + list(it) == list(range(3, 10)) * 2


def test_chainable_iterable():
    it = range(10)
    it = IterableElemMap(it, lambda x: x + 11)
    assert list(it) + list(it) == list(range(11, 21)) * 2


def test_IterableElemMap_init():
    func = lambda x: x + 1
    obj = IterableElemMap([1, 2, 3], func)
    assert obj.source == [1, 2, 3]
    assert id(obj.operation) == id(func)


def test_IterableElemMap_init2():
    res = IterableElemMap([1, 2, 3])
    assert res.source == [1, 2, 3]
    assert res.operation is not None


def test_IterableElemMap_fmap():
    obj = IterableElemMap([1, 2, 3], lambda x: x + 1)
    obj2 = obj.fmap([2, 3])
    assert obj2.operation == [2, 3]


def test_IterableElemMap_unbox():
    obj = IterableElemMap([1, 2, 3], lambda x: x + 1)
    y = 2
    for x in obj.unbox():
        assert x == y
        y += 1


def test_IterableElemMap_empty():
    res = IterableElemMap.empty()
    assert type(res.source) == tuple


# TODO(NameError: name 'ItertoolsIterable' is not defined)
@pytest.mark.skip("not implemented yet.")
def test_IterableElemMap_extend():
    pass


# TODO(NameError: name 'ItertoolsIterable' is not defined)
@pytest.mark.skip("not implemented yet.")
def test_IterableElemMap_filter():
    pass


def test_IterableIterMap_init():
    func = lambda x: x + 1
    obj = IterableIterMap([1, 2, 3], func)
    assert obj.source == [1, 2, 3]
    assert id(obj.operation) == id(func)


def test_IterableIterMap_init2():
    res = IterableIterMap([1, 2, 3])
    assert res.source == [1, 2, 3]
    assert res.operation is not None


# TODO（NameError: name 'ItertoolsIterable' is not defined）
@pytest.mark.skip("not implemented yet.")
def test_IterableIterMap_fmap():
    pass


def test_IterableIterMap_unbox():
    def func(y):
        return [x for x in y]

    obj = IterableIterMap([1, 2, 3], func)
    res = obj.unbox()
    z = 1
    for x in res:
        assert x == z
        z += 1


# TODO（NameError: name 'ItertoolsIterable' is not defined）
@pytest.mark.skip("not implemented yet.")
def test_IterableIterMap_extend():
    pass


# TODO（NameError: name 'ItertoolsIterable' is not defined）
@pytest.mark.skip("not implemented yet.")
def test_IterableIterMap_filter():
    pass


def test_empty():
    res = IterableIterMap.empty()
    assert type(res.source) == tuple

# def test_Count_init():
#     count = Count([1],[2])
#     assert count.start == [1]
#     assert count.step == [2]


#TODO(The abc in on_collections.py:32 does not exist.)
@pytest.mark.skip("not implemented yet.")
def test_take_():
    pass