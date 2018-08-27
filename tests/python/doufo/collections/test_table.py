import pytest
from doufo.collections import Table

class TableSon(Table):

	def fmap(self, f):
		...


def test_eq():
	assert TableSon(1, 2).source == 1


def test_eq2():
	assert TableSon(1, 2).dataclass == None


def test_getitem_int():
	assert TableSon([1, 2, 3], [3, 4])[0] == 1


def test_getitem_int2():
	assert TableSon([1, 2, 3], [3, 4])[1] == 2


def test_getitem_int3():
	assert TableSon([1, 2, 3], [3, 4])[:2] == [1, 2]


def test_getitem_slice_class():
	assert isinstance(TableSon([1, 2, 3], [3, 4])[:2], Table)
