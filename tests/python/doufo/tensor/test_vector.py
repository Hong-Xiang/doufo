from doufo.tensor import project, all_close, Vector


def test_project_withvalue():
    v1 = Vector([1.0, 0.0])
    v2 = Vector([1.0, 1.0])
    assert all_close(project(v1, v2), Vector([0.5, -0.5]))


def test_project_withoutvalue():
    v1 = Vector([1.0, 0.0])
    v2 = Vector([0.0, 1.0])
    assert all_close(project(v1, v2), Vector([1.0, 0.0]))


def test_project_keep_scale():
    v1 = Vector([3.0, 0.0])
    v2 = Vector([1.0, 1.0])
    assert all_close(project(v1, v2), Vector([1.5, -1.5]))

def test_slice():
    v = Vector([1.0, 2.0])
    assert v[0] == 1.0