import pytest

from mo import mofile


def test_load_success():
    assert mofile.load('Mofile')


def test_load_non_existent():
    with pytest.raises(FileNotFoundError):
        mofile.load('Mofile.does.not.exist')
