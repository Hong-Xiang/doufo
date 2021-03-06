from doufo.function import WrappedFunction, Function, func, singledispatch, multidispatch, tagfunc, fmap, filter_, pass_key
from doufo.function import nargs, ndefs


def test_currying():
    def foo_(a, b, c):
        return a + b + c

    foo = WrappedFunction(foo_)
    f1 = foo(1)
    f2 = f1(2)
    v = f2(3)
    assert v == 6
    assert f2(4) == 7
    assert f1(7, 9) == 17
    assert foo(1, 4, 6) == 11


def test_func_deco():
    @func()
    def foo(a, b):
        return a + b

    assert foo(1)(2) == 3


def test_func_nargs():
    @func(2)
    def foo(a, b):
        return a + b

    assert foo(2)(3) == 5


def test_func_nargs_none():
    @func()
    def foo(a, b):
        return a + b

    assert foo(2)(3) == 5


def test_func_not_inferable():
    @func()
    def foo(*args):
        return sum(args)

    assert foo(2) == 2


def test_bind():
    @func()
    def foo(a):
        return a + 1

    @func()
    def bar(a):
        return a * 2

    assert (foo >> bar)(3) == 8


def test_guess_nargs():
    def foo(a, b):
        pass

    assert nargs(foo) == 2


def test_nouts():
    @func(nargs=2, nouts=2)
    def foo(a, b):
        return a + 1, b + 1

    assert (foo >> foo)(1, 2) == (3, 4)


def test_guess_nargs_with_defaults():
    def foo(a, b=1):
        pass

    assert nargs(foo) == 2
    assert ndefs(foo) == 1


def test_single_dispatch_construct():
    @singledispatch()
    def foo(a, b):
        return a + b

    @foo.register(int)
    def _(a, b):
        return a * b

    @foo.register(str)
    def _(a, b):
        return a + b * 2

    assert foo(3, 6) == 18
    assert foo('1', '2') == '122'
    assert foo([1], [2]) == [1, 2]


def test_multidispatch():
    @multidispatch()
    def foo(a, b):
        return a + b

    @foo.register(int, int)
    def _(a, b):
        return a * b

    @foo.register(str, str)
    def _(a, b):
        return a + b * 2

    @foo.register(str, int)
    def _(a, b):
        return int(a) + b * 3

    assert foo(3, 4) == 12
    assert foo('1', '2') == '122'
    assert foo('1', 3) == 10
    assert foo([1], [2, 3]) == [1, 2, 3]


def test_tagfunc():
    @tagfunc()
    def foo(a, b):
        return a + b

    @foo.register(int)
    def _(a, b):
        return a * b

    @foo.register(str)
    def _(a, b):
        return a + b * 2

    assert foo[int](3, 6) == 18
    assert foo[str]('1', '2') == '122'
    assert foo[str](3, 6) == 15
    assert foo([1], [2]) == [1, 2]


def test_fmap_list():
    assert fmap(lambda x: x+1, [1, 2, 3]) == [2, 3, 4]


def test_fmap_tuple():
    assert fmap(lambda x: x+1, (1, 2, 3)) == (2, 3, 4)


def test_fmap_dict_full():
    assert fmap(lambda k, v: (k, v + 1), {'a': 1, 'b': 2}) == {'a': 2, 'b': 3}


def test_fmap_dict_no_key():
    assert fmap(pass_key(lambda x: x + 1),
                {'a': 1, 'b': 2}) == {'a': 2, 'b': 3}


def test_filter_list():
    assert filter_(lambda x: x % 2 == 1, [1, 2, 3]) == [1, 3]


def test_filter_tuple():
    assert filter_(lambda x: x % 2 == 1, (1, 2, 3)) == (1, 3)


def test_filter_dict_full():
    assert filter_(lambda k, v: v % 2 == 1, {'a': 1, 'b': 2}) == {'a': 1}
