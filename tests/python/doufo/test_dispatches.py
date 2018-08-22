from doufo.dispatches import singledispatch


def test_singledispatch():
    @singledispatch()
    def goo(a, b):
        return a + b

    @goo.register(int)
    def _(a, b):
        return a + 2 * b

    assert goo(1)(2) == 5
    assert goo(1, 2) == 5
    assert goo('1')('2') == '12'
    assert goo('1', '2') == '12'
