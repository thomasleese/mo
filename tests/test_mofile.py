import pytest

from mo import mofile


def test_load_yaml():
    assert mofile.load('tests/examples/mofile.yaml', format='yaml')


def test_load_toml():
    assert mofile.load('tests/examples/mofile.toml', format='toml')


def test_load_json():
    assert mofile.load('tests/examples/mofile.json', format='json')


def test_load_auto():
    assert mofile.load('tests/examples/mofile.yaml')
    assert mofile.load('tests/examples/mofile.toml')
    assert mofile.load('tests/examples/mofile.json')


def test_invalid_format():
    with pytest.raises(mofile.InvalidMofileFormat):
        mofile.load('tests/examples/mofile.txt')


def test_load_non_existent():
    with pytest.raises(FileNotFoundError):
        mofile.load('Mofile.does.not.exist')
