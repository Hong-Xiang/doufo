from dxl.data import DataClass
from dxl.data.collections.dataclass import DataList, DataArray
from dxl.function.collections.dataclass import list_of_dataclass_to_numpy_structure_of_array
from dxl.function.dataclass import replace
import operator
import numpy as np


def test_aos_soa_campat():
    class C(DataClass):
        __slots__ = ('a', 'b')
    aos = DataList(C, [C(1, 2), C(3, 4), C(5, 6)])
    soa = DataArray(C, list_of_dataclass_to_numpy_structure_of_array(
        aos, [np.int32, np.int32]))
    aos.filter(lambda c: c.a >= 3)
    aos.fmap(lambda c: c.a)
    aos.fmap(lambda c: replace(c, a=c.a + 1))
    soa.filter(lambda c: c.a >= 3)
    soa.fmap(lambda c: c.a)
    soa.fmap(lambda c: replace(c, a=c.a + 1))
