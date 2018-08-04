from doufo import PureFunction, func


def test_currying():
    def foo_(a, b, c):
        return a + b + c
    foo = PureFunction(foo_)
    f1 = foo(1)
    f2 = f1(2)
    v = f2(3)
    assert v == 6
    assert f2(4) == 7
    assert f1(7, 9) == 17
    assert foo(1, 4, 6) == 11


def test_func_deco():
    @func
    def foo(a, b):
        return a + b
    assert foo(1)(2) == 3


def test_bind():
    @func
    def foo(a):
        return a + 1

    @func
    def bar(a):
        return a * 2

    assert (foo >> bar)(3) == 8
