from doufo import PureFunction, func, singledispatch
from doufo.function import guess_nargs


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


def test_singledispatch():
    @singledispatch
    def goo(a, b):
        return a + b

    @goo.register(int)
    def _(a, b):
        return a + 2 * b

    assert goo(1)(2) == 5
    assert goo(1, 2) == 5
    assert goo('1')('2') == '12'
    assert goo('1', '2') == '12'


def test_guess_nargs():
    def foo(a, b):
        pass
    assert guess_nargs(foo) == 2


def test_guess_nargs_with_defaults():
    def foo(a, b=1):
        pass
    assert guess_nargs(foo) == 1
