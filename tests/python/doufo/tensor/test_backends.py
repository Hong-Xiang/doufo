def test_import_backend():
    import doufo.tensor.backends 
    assert "backend" in doufo.tensor.backends.__all__
