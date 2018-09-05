from doufo import List
from doufo import head


def test_eq():
    assert List([1, 2]) == [1, 2]


def test_eq_List():
    assert List([1, 2]) == List([1, 2])


def test_wrap_construct():
    a = List([1, 2])
    assert List(a) == [1, 2]


def test_wrap_construct_List():
    a = List(List([1, 2]))
    assert a == [1, 2]


def test_fmap_value():
    assert List[int]([1, 2]).fmap(lambda x: x + 1) == [2, 3]


def test_fmap_type():
    assert isinstance(List[int]([1, 2]).fmap(lambda x: x + 1), List)


def test_add_value():
    assert List([1]) + List([2]) == [1, 2]


def test_add_type():
    assert isinstance(List([1]) + List([2]), List)


def test_getitem_int():
    assert List([1, 2])[0] == 1


def test_getitem_slice_value():
    assert List([1, 2, 3])[:2] == [1, 2]


def test_getitem_slice_class():
    assert isinstance(List([1, 2, 3])[:2], List)


def test_head():
    assert head(List([1, 2])) == 1


def test_filter():
    assert List([1, 2, 3, 4, 5, 6]).filter(lambda x: x < 4) == [1, 2, 3]
