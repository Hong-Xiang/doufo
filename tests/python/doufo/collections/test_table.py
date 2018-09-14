import pytest
from doufo.collections import Table


class DummyTable(Table):

	def fmap(self, f):
		...


def test_init():
	assert DummyTable(1, 2).source == 1


def test_init2():
	assert DummyTable(1, 2).dataclass is None


def test_getitem_int():
	assert DummyTable([1, 2, 3], [3, 4])[0] == 1


def test_getitem_int2():
	assert DummyTable([1, 2, 3], [3, 4])[1] == 2


def test_getitem_int3():
	assert DummyTable([1, 2, 3], [3, 4])[:2] == [1, 2]


# def test_getitem_slice_class():
# 	assert isinstance(DummyTable([1, 2, 3], [3, 4])[:2], Table)
