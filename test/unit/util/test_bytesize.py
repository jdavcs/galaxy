import pytest

from galaxy.util.bytesize import ByteSize, parse_bytesize


def test_parse_bytesize_int_or_float():
    assert parse_bytesize(42) == 42
    assert parse_bytesize(42.5) == 42.5


def test_parse_bytesize_str_no_suffix():
    assert parse_bytesize('42') == 42
    assert parse_bytesize('42.5') == 42.5


def test_parse_bytesize_str_suffix():
    assert parse_bytesize('10K') == 10000
    assert parse_bytesize('10 KI') == 10240


def test_parse_bytesize_str_invalid():
    with pytest.raises(ValueError):
        parse_bytesize('10 invalid-suffix')
    with pytest.raises(ValueError):
        parse_bytesize('invalid-value')


def test_bytesize_to_unit():
    bs = ByteSize(1_000_000_000_000_000)
    assert bs.to_unit('k') == '1000000000000K'
    assert bs.to_unit('m') == '1000000000M'
    assert bs.to_unit('g') == '1000000G'
    assert bs.to_unit('t') == '1000T'
    assert bs.to_unit('p') == '1P'
    assert bs.to_unit('e') == '0E'

    assert bs.to_unit('ki') == '976562500000KI'
    assert bs.to_unit('mi') == '953674316MI'
    assert bs.to_unit('gi') == '931322GI'
    assert bs.to_unit('ti') == '909TI'
    assert bs.to_unit('pi') == '0PI'
    assert bs.to_unit('ei') == '0EI'

    assert bs.to_unit() == '1000000000000000'  # no unit
    assert bs.to_unit('K') == '1000000000000K'  # uppercase unit


def test_bytesize_to_unit_as_str():
    bs = ByteSize(1_000_000_000_000_000)
    assert bs.to_unit('k', as_string=False) == 1000000000000  # not to_string


def test_bytesize_to_unit_invalid():
    bs = ByteSize(1_000_000_000_000_000)
    with pytest.raises(KeyError):
        bs.to_unit('invalid')


@pytest.mark.parametrize(
    "unit, expected_value",
    [
        ('k', '1000000000000K'),
        ('m', '1000000000M'),
        ('g', '1000000G'),
        ('t', '1000T'),
        ('p', '1P'),
        ('e', '0E'),
        ('ki', '976562500000KI'),
        ('mi', '953674316MI'),
        ('gi', '931322GI'),
        ('ti', '909TI'),
        ('pi', '0PI'),
        ('ei', '0EI'),
        (None, '1000000000000000'),
        ('K', '1000000000000K'),
    ]
)
def test_bytesize_to_unit_better(unit, expected_value):
    bs = ByteSize(1_000_000_000_000_000)
    assert bs.to_unit(unit) == expected_value
