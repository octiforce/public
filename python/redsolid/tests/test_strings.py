"""Tests for the redsolid.strings module."""
# Lint: Docstrings are not required for test functions.
# pylint: disable=missing-function-docstring


import math
from types import NoneType

from redsolid.strings import (
    str_cast,
    str_is_bool,
    str_is_float,
    str_is_int,
    str_is_none,
    str_type,
)


def test_str_is_none() -> None:
    assert str_is_none("None")
    assert str_is_none(" none ")
    assert str_is_none("Null")
    assert str_is_none(" null ")
    assert str_is_none("")
    assert str_is_none("  ", allow_empty=True)
    assert not str_is_none("", allow_empty=False)
    assert not str_is_none("False")
    assert not str_is_none("0")
    assert not str_is_none("0.0")
    assert not str_is_none("xyz")


def test_str_is_bool() -> None:
    assert str_is_bool("True")
    assert str_is_bool(" true ")
    assert str_is_bool("False")
    assert str_is_bool(" false ")
    assert not str_is_bool("None")
    assert not str_is_bool("")
    assert not str_is_bool("1")
    assert not str_is_bool("1.0")
    assert not str_is_bool("xyz")


def test_str_is_int() -> None:
    assert str_is_int("+123")
    assert str_is_int(" -123 ", base=10)
    assert str_is_int("0b0101")
    assert str_is_int("-0101  ", base=2)
    assert not str_is_int("  102", base=2)
    assert str_is_int("0o1357")
    assert str_is_int("-1357  ", base=8)
    assert not str_is_int("  1358", base=8)
    assert str_is_int("0x37bF")
    assert str_is_int("-37bF  ", base=16)
    assert not str_is_int("  37bG", base=16)
    assert not str_is_int("None")
    assert not str_is_int("")
    assert not str_is_int("True")
    assert not str_is_int("123.45")
    assert not str_is_int("xyz")


def test_str_is_float() -> None:
    assert str_is_float("123.45")
    assert str_is_float("-12.345e+1")
    assert str_is_float("  +1234.5e-1")
    assert str_is_float("+1234.5e-1  ")
    assert str_is_float(" NaN")
    assert str_is_float("nan ", allow_non_finite=True)
    assert not str_is_float("+Inf", allow_non_finite=False)
    assert not str_is_float("-Inf", allow_non_finite=False)
    assert not str_is_float("123")
    assert str_is_float("123", allow_int=True)
    assert not str_is_float("None")
    assert not str_is_float("")
    assert not str_is_float("True")
    assert not str_is_float("xyz")


def test_str_type() -> None:
    assert str_type("None") is NoneType
    assert str_type("Null") is NoneType
    assert str_type("") is NoneType
    assert str_type("", empty_is_none=False) is str
    assert str_type("True") is bool
    assert str_type("False") is bool
    assert str_type("123") is int
    assert str_type("0x37bf") is int
    assert str_type("37bf") is str
    assert str_type("37bf", int_base=16) is int
    assert str_type("123.45") is float
    assert str_type("NaN") is float
    assert str_type("NaN", allow_non_finite_float=False) is str
    assert str_type("xyz") is str


def test_str_cast() -> None:
    assert str_cast("None") is None
    assert str_cast("Null") is None
    assert str_cast("") is None
    assert str_cast("", empty_is_none=False) == ""
    assert str_cast("True") is True
    assert str_cast("False") is False
    assert str_cast("123") == 123
    assert str_cast("0x37bf") == 14271
    assert str_cast("37bf") == "37bf"
    assert str_cast("37bf", int_base=16) == 14271
    assert str_cast("12.345") == 12.345
    assert str_cast("xyz") == "xyz"

    result = str_cast("NaN")
    assert isinstance(result, float)
    assert math.isnan(result)
    assert str_cast("NaN", allow_non_finite_float=False) == "NaN"
