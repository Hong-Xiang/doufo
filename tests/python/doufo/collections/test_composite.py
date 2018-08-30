import pytest
from itertools import chain
from doufo.collections import CompositeSequence, List


class DummyCompositeSequence(CompositeSequence):

	def fmap(self, f):
		...

	def empty(cls):
		...

	def extend(self, f):
		...


def test_init():
	assert DummyCompositeSequence([[1, 2], [3, 4]]).sources == List([[1, 2], [3, 4]])


def test_init2():
	assert not DummyCompositeSequence([[1, 2], [3, 4]]).sources == List([[2, 2], [3, 4]])


def test_iter():
	assert [x for x in iter(DummyCompositeSequence([[1, 2], [3, 4]]))] == [1, 2, 3, 4]


def test_len():
	assert len(DummyCompositeSequence([[1, 2], [3, 4]])) == 4


def test_unbox():
	assert DummyCompositeSequence([[1, 2], [3, 4]]).unbox() == [[1, 2], [3, 4]]
