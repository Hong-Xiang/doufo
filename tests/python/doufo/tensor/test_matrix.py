from doufo.tensor import Matrix, Vector, all_close


def test_matmul_mv():
    result = Matrix([[1, 2], [3, 4], [5, 6]]) @ Vector([7, 8])
    assert isinstance(result, Vector)
    assert all_close(result, Vector([23, 53, 83]))


def test_matmul_vm():
    result = Vector([7, 8, 9]) @ Matrix([[1, 2], [3, 4], [5, 6]])
    assert isinstance(result, Vector)
    assert all_close(result, Vector([76, 100]))
