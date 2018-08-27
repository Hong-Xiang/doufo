import pytest
from itertools import chain
from doufo.collections import CompositeSequence


class ComSeq(CompositeSequence):

	def fmap(self, f):
		...

	def empty(cls):
		...

	def extend(self, f):
		...


def test_eq():
	assert ComSeq([[1, 2], [3, 4]]).sources == ComSeq([[1, 2], [3, 4]]).sources


def test_neq():
	assert not ComSeq([[1, 2], [3, 4]]).sources == ComSeq([[0, 2], [3, 4]]).sources


def test_iter():
	assert [x for x in iter(ComSeq([[1, 2], [3, 4]]))] == [1, 2, 3, 4]


def test_len():
	assert len(ComSeq([[1, 2], [3, 4]])) == 4


def test_unbox():
	assert ComSeq([[1, 2], [3, 4]]).unbox() == [[1, 2], [3, 4]]
