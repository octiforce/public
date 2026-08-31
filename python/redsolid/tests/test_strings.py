"""Tests for the redsolid.strings module."""
# Lint: Docstrings are not required for test functions.
# pylint: disable=missing-function-docstring


from redsolid.strings import (
    str_from_iterable,
    str_to_list,
)


def test_str_from_iterable() -> None:
    test_list = [1, 2, 3]
    test_tuple = (None, True, 6, 4.5, "xyz")
    assert str_from_iterable(test_list) == "1\n2\n3"
    assert str_from_iterable(test_list, sep=", ") == "1, 2, 3"
    assert str_from_iterable(test_tuple) == "None\nTrue\n6\n4.5\nxyz"
    assert str_from_iterable(test_tuple, sep=", ") == (
        "None, True, 6, 4.5, xyz"
    )


def test_str_to_list() -> None:
    assert str_to_list("None\nTrue") == ["None", "True"]
  # assert str_to_list(" True : true: False: 0 ", sep=":", converter=bool) == [
    #     True, True, False, False
    # ]
   # assert str_to_list(" 1,2,3, 5,8, 0xd, 0o25 ", sep=",", converter=int) == [
    #     1, 2, 3, 5, 8, 13, 21
    # ]
    # assert str_to_list(
    #     " 1,2,3, 5,8, 0xd, 0o25 ", sep=",", converter=int, strip=False
    # ) == [1, 2, 3, 5, 8, 13, 21]
  # assert str_to_list(" 1.25  2.5   3.75  1e2", sep=" ", converter=float) == [
    #     1.25, 2.5, 3.75, 100
    # ]
    # assert str_to_list(
    #     " 1.25  2.5   3.75  1e2", sep=" ", converter=float, strip=False
    # ) == [1.25, 2.5, 3.75, 100]
    # assert str_to_list(" abc , def , ghi ", sep=",") == ["abc", "def", "ghi"]
    # assert str_to_list(" abc , def , ghi ", sep=",", strip=False) == [
    #     " abc ", " def ", " ghi "]


# def test_str_from_mapping() -> None:
#     test_dict = {"n": None, "b": True, "i": 6, "f": 4.5, "s": "xyz"}
#     assert str_from_mapping(test_dict) == "n:None\nb:True\ni:6\nf:4.5\ns:xyz"
#     assert str_from_mapping(test_dict, sep=", ", link=" -> ") == (
#         "n -> None, b -> True, i -> 6, f -> 4.5, s -> xyz"
#     )
