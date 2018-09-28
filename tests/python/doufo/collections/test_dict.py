from doufo.collections.dict import *

dct = Dict([['1', '2'], ['2', '3']])


def func(v):
    return v + "1"


def test_fmap():
    assert dct.fmap(func) == {'1': '21', '2': '31'}


def test_unbox():
    assert dct.data == {'1': '2', '2': '3'}
