from doufo.utils import *

def test_method_not_support_msg():
    res = method_not_support_msg(1,1)
    assert res == "1 for <class 'int'> is not implemented yet."
