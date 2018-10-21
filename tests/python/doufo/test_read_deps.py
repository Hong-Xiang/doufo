from doufo.read_deps import *

import os
import re

from doufo.read_deps import GetFileList


def test_GetFileList():
    res = GetFileList()
    for fextension in res[0]:
        root = os.path.splitext(fextension)
        assert root[1] == '.py'
        assert 'test' not in root
        assert '__' not in root
    for dir in res[0]:
        if 'test' not in dir:
            assert 'test' not in dir
        else:
            for single in dir.split('/'):
                assert single != 'test'
        assert '__' not in dir
        assert '/.' not in dir


# def test_FindModuleLocations():
#     res = FindModuleLocations()
#     for key, value in res.items():
#         assert key[0:5] == MOD_NAME
#         assert type(value) == list
#         assert value == []
