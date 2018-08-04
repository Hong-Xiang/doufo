from doufo.tensor import Tensor, all_close


def test_add():
    a, b = Tensor([1, 2]), Tensor([3, 4])
    c = Tensor([4, 6])
    assert all_close(a + b, c)


def test_len():
    assert len(Tensor([1, 2, 3])) == 3
