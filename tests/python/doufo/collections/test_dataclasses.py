from doufo import dataclass, replace
from doufo.collections import DataList, DataArray, list_of_dataclass_to_numpy_structure_of_array
import operator
import numpy as np
import attr


def test_aos_soa_campat():
    @dataclass
    class C:
        a: int
        b: int
    aos = DataList([C(1, 2), C(3, 4), C(5, 6)])
    soa = DataArray(list_of_dataclass_to_numpy_structure_of_array(aos), C)
    aos.filter(lambda c: c.a >= 3)
    aos.fmap(lambda c: c.a)
    aos.fmap(lambda c: replace(c, a=c.a + 1))
    soa.filter(lambda c: c.a >= 3)
    soa.fmap(lambda c: c.a)
    soa.fmap(lambda c: replace(c, a=c.a + 1))

