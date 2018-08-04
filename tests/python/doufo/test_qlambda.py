from doufo import x


def test_getattr():
    f = x.a

    class T:
        a = 1
    assert f(T()) == 1


def test_slice():
    f = x[1]
    assert f([1, 2, 3]) == 2


def test_eq():
    f = (x == 3)
    assert f(3)
    assert not f(2)


def test_chain_slice_eq():
    assert (x[1] == 3)([1, 3, 1])
    assert not (x[1] == 3)([1, 1])


def test_add():
    assert list(map(x + 1, [1, 2, 3])) == [2, 3, 4]


def test_sub():
    assert list(map(x - 1, [1, 2, 3])) == [0, 1, 2]
