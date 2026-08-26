"""String transformation and formatting solutions."""


from __future__ import annotations

import math
from collections.abc import Callable, Generator, Iterable, Iterator, Mapping
from contextlib import contextmanager
from types import NoneType
from typing import Any, TypeVar, overload, override


_K = TypeVar("_K")
"""Invariant type variable for a mutable mapping key."""
_T = TypeVar("_T")
"""Invariant type variable for a mutable value."""


class Indenter:
    """
    Indents strings and tracks indentation level for nested output.

    Indenters are initialized with default indenting step text (4 spaces
    unless specified).  The push() and pop() methods add or remove one
    or more indent levels.  The indent() method will return a string
    that is prefixed with the indentation steps.
    """

    def __init__(self, *, default_step: str = "    ") -> None:
        """Initialize the indenter."""
        if not default_step:
            raise ValueError(
                "Argument 'default_step' cannot be an empty string."
            )
        self._default_step = default_step
        self._steps: list[str] = []
        self._prefix = ""

    @override
    def __repr__(self) -> str:
        """Get a debug string representation."""
        return (
            f"{type(self).__name__}(default_step={self.default_step!r}, "
            f"steps={self.steps!r}, prefix={self.prefix!r})"
        )

    @override
    def __str__(self) -> str:
        """Get a user string representation."""
        return self._prefix

    @property
    def default_step(self) -> str:
        """Get the default step text used for one indent level."""
        return self._default_step

    @property
    def steps(self) -> tuple[str, ...]:
        """Get the sequence of steps used for current indentation."""
        return tuple(self._steps)

    @property
    def level(self) -> int:
        """Get the number of steps used for the current indentation."""
        return len(self._steps)

    @property
    def prefix(self) -> str:
        """Get the combined text of steps for current indentation."""
        return self._prefix

    def push(
            self, *, step_count: int = 1, custom_step: str | None = None
    ) -> None:
        """
        Increase (push) the indentation level by one or more steps.

        By default, the indentation is increased by one step.  The
        default step text is used for indenting the new level(s) unless
        a custom step is specified.
        """
        if step_count <= 0:
            raise ValueError(
                "Argument 'step_count' must be greater than zero."
            )
        if custom_step == "":
            raise ValueError(
                "Argument 'custom_step' cannot be an empty string."
            )
        step = self._default_step if custom_step is None else custom_step
        self._steps.extend([step] * step_count)
        self._prefix = "".join(self._steps)

    def pop(self, *, step_count: int = 1) -> None:
        """
        Decrease (pop) the indentation level by one or more steps.

        By default, the indentation is decreased by one step.  Raises
        ValueError if step_count exceeds the current indentation level.
        """
        if step_count <= 0:
            raise ValueError(
                "Argument 'step_count' must be greater than zero."
            )
        if step_count > self.level:
            raise ValueError(
                f"Attempted to pop {step_count} indent step(s), but current "
                f"indent level ({self.level}) is too low."
            )
        del self._steps[-step_count:]
        self._prefix = "".join(self._steps)

    def indent(self, value: Any) -> str:
        """
        Format a value with the current indentation prefix.

        If the value to indent is a multi-line string, each line is
        prefixed with the current indentation.  If there is a trailing
        newline, it is preserved without adding indentation after it.
        """
        lines = str(value).split("\n")
        if lines[-1]:
            result = "\n".join(f"{self.prefix}{line}" for line in lines)
        else:
            result = (
                "\n".join(f"{self.prefix}{line}" for line in lines[:-1]) + "\n"
            )
        return result

    @contextmanager
    def indented(
            self, *, step_count: int = 1, custom_step: str | None = None
    ) -> Generator[Indenter, None, None]:
        """
        Temporarily increase the indentation level by one or more steps.

        Prior indentation is automatically restored when the context is
        exited, including if an exception occurs.
        """
        self.push(custom_step=custom_step, step_count=step_count)
        try:
            yield self
        finally:
            self.pop(step_count=step_count)


def str_from_iterable(items: Iterable[Any], *, sep: str = "\n") -> str:
    """
    Convert any Iterable into a simple separated string.

    The returned string contains all items converted to strings,
    each separated by a separator string (default is newline).
    """
    _validate_not_empty(sep)
    return sep.join(str(item) for item in items)


@overload
def str_to_list(
        text: str, *, sep: str = "\n", converter: Callable[[str], str] = str,
        strip: bool = True
) -> list[str]:
    """Convert a simple separated string into a list."""
    # Lint: Overloads require a docstring and an ellipsis.
    ...  # pylint: disable=unnecessary-ellipsis  # noqa: PIE790


@overload
def str_to_list(
        text: str, *, sep: str = "\n", converter: Callable[[str], _T],
        strip: bool = True
) -> list[_T]:
    """Convert a simple separated string into a list."""
    # Lint: Overloads require a docstring and an ellipsis.
    ...  # pylint: disable=unnecessary-ellipsis  # noqa: PIE790


def str_to_list(
        text: str, *, sep: str = "\n", converter: Callable[[str], Any] = str,
        strip: bool = True
) -> list[Any]:
    """
    Convert a simple separated string into a list.

    The returned list contains all items extracted from the string,
    delimited by a separator (default is newline).

    Each item is converted with the specified converter, which
    defaults to str.  The converter can be any callable that accepts
    a single string argument, including basic types such as bool,
    float, and int.

    If strip is set to True (default), then whitespace is stripped
    from before and after each item, and any items that are empty
    after stripping are ignored.
    """
    _validate_not_empty(sep)
    item_strs = _get_item_strs(text, sep, strip)
    return [
        converter(item_str) for item_str in item_strs
        if item_str != "" or not strip
    ]


@overload
def str_to_tuple(
        text: str, *, sep: str = "\n", converter: Callable[[str], str] = str,
        strip: bool = True
) -> tuple[str]:
    """Convert a simple separated string into a tuple."""
    # Lint: Overloads require a docstring and an ellipsis.
    ...  # pylint: disable=unnecessary-ellipsis  # noqa: PIE790


@overload
def str_to_tuple(
        text: str, *, sep: str = "\n", converter: Callable[[str], _T],
        strip: bool = True
) -> tuple[_T]:
    """Convert a simple separated string into a tuple."""
    # Lint: Overloads require a docstring and an ellipsis.
    ...  # pylint: disable=unnecessary-ellipsis  # noqa: PIE790


def str_to_tuple(
        text: str, *, sep: str = "\n", converter: Callable[[str], Any] = str,
        strip: bool = True
) -> tuple[Any, ...]:
    """
    Convert a simple separated string into a tuple.

    The returned tuple contains all items extracted from the string,
    delimited by a separator (default is newline).

    Each item is converted with the specified converter, which
    defaults to str.  The converter can be any callable that accepts
    a single string argument, including basic types such as bool,
    float, and int.

    If strip is set to True (default), then whitespace is stripped
    from before and after each item, and any items that are empty
    after stripping are ignored.
    """
    _validate_not_empty(sep)
    item_strs = _get_item_strs(text, sep, strip)
    return tuple(
        converter(item_str) for item_str in item_strs
        if item_str != "" or not strip
    )


@overload
def str_to_set(
        text: str, *, sep: str = "\n", converter: Callable[[str], str] = str,
        strip: bool = True
) -> set[str]:
    """Convert a simple separated string into a set."""
    # Lint: Overloads require a docstring and an ellipsis.
    ...  # pylint: disable=unnecessary-ellipsis  # noqa: PIE790


@overload
def str_to_set(
        text: str, *, sep: str = "\n", converter: Callable[[str], _T],
        strip: bool = True
) -> set[_T]:
    """Convert a simple separated string into a set."""
    # Lint: Overloads require a docstring and an ellipsis.
    ...  # pylint: disable=unnecessary-ellipsis  # noqa: PIE790


def str_to_set(
        text: str, *, sep: str = "\n", converter: Callable[[str], Any] = str,
        strip: bool = True
) -> set[Any]:
    """
    Convert a simple separated string into a set.

    The returned set contains all items extracted from the string,
    delimited by a separator (default is newline).  Like any set,
    duplicate items are removed.

    Each item is converted with the specified converter, which
    defaults to str.  The converter can be any callable that accepts
    a single string argument, including basic types such as bool,
    float, and int.

    If strip is set to True (default), then whitespace is stripped
    from before and after each item, and any items that are empty
    after stripping are ignored.
    """
    _validate_not_empty(sep)
    item_strs = _get_item_strs(text, sep, strip)
    return {
        converter(item_str) for item_str in item_strs
        if item_str != "" or not strip
    }


def str_from_mapping(
        items: Mapping[Any, Any], *, sep: str = "\n", link: str = ":"
) -> str:
    """
    Convert any Mapping into a simple separated string.

    The returned string contains all key/value entries converted to
    strings.  Each key and value is separated by a link string
    (default is ":"), then each entry is separated by a separator
    string (default is newline).
    """
    _validate_not_empty(sep, link)
    return sep.join(f"{key}{link}{value}" for key, value in items.items())


@overload
# Lint: Larger number of arguments is required for this method.
# pylint: disable=too-many-arguments
def str_to_dict(
    text: str, *, sep: str = "\n", link: str = ":",
    key_converter: Callable[[str], str] = str,
    value_converter: Callable[[str], str] = str, strip: bool = True
) -> dict[str, str]:
    # Lint: Overloads require a docstring and an ellipsis.
    ...  # pylint: disable=unnecessary-ellipsis  # noqa: PIE790


@overload
# Lint: Larger number of arguments is required for this method.
# pylint: disable=too-many-arguments
def str_to_dict(
    text: str, *, sep: str = "\n", link: str = ":",
    key_converter: Callable[[str], str] = str,
    value_converter: Callable[[str], _T], strip: bool = True
) -> dict[str, _T]:
    # Lint: Overloads require a docstring and an ellipsis.
    ...  # pylint: disable=unnecessary-ellipsis  # noqa: PIE790


@overload
# Lint: Larger number of arguments is required for this method.
# pylint: disable=too-many-arguments
def str_to_dict(
    text: str, *, sep: str = "\n", link: str = ":",
    key_converter: Callable[[str], _K], value_converter: Callable[[str], _T],
    strip: bool = True
) -> dict[_K, _T]:
    # Lint: Overloads require a docstring and an ellipsis.
    ...  # pylint: disable=unnecessary-ellipsis  # noqa: PIE790


# Lint: Larger number of arguments is required for this method.
# pylint: disable=too-many-arguments
def str_to_dict(
    text: str, *, sep: str = "\n", link: str = ":",
    key_converter: Callable[[str], Any] = str,
    value_converter: Callable[[str], Any] = str, strip: bool = True
) -> dict[Any, Any]:
    """
    Convert a simple separated string into a dict.

    The returned dict contains all key/value entries extracted from
    the string, delimited first by an entry separator (default is
    newline) and then the separating link string between key and
    value (default is ":").  If the link string appears more than
    once in an entry, only the first link is used to separate key
    and value.

    Keys and values are converted with their specified converters,
    which both default to str.  A converter can be any callable that
    accepts a single string argument, including basic types such as
    bool, float, and int.

    If strip is set to True (default), then whitespace is stripped
    from before and after each key and each value.  Empty entries
    with no link are ignored when strip is True.  If the link
    string is present, but either the key or the value is empty,
    conversion will still be attempted on the empty key or value.
    """
    _validate_not_empty(sep, link)
    item_strs = _get_item_strs(text, sep, strip)
    items: dict[Any, Any] = {}
    for item_str in item_strs:
        if not item_str and strip:
            continue
        link_index = item_str.find(link)
        if link_index == -1:
            raise ValueError(
                f"Entry {item_str!r} does not contain link string {link!r}."
            )
        key_str = item_str[:link_index]
        value_str = item_str[link_index + len(link):]
        if strip:
            key_str = key_str.strip()
            value_str = value_str.strip()
        key = key_converter(key_str)
        value = value_converter(value_str)
        items[key] = value
    return items


def str_is_none(text: str, *, allow_empty: bool = True) -> bool:
    """
    Determine if a string represents a None value.

    The strings "none" and "null", ignoring case and surrounding
    whitespace, are always recognized as None values.  If allow_empty is
    True (default), an empty or whitespace-only string is also
    recognized as a None value.
    """
    normalized_text = text.strip().lower()
    return (
        normalized_text in ("none", "null")
        or (allow_empty and not normalized_text)
    )


def str_is_bool(text: str) -> bool:
    """
    Determine if a string represents a Boolean value.

    The strings "true" and "false", ignoring case and surrounding
    whitespace, are always recognized as Boolean values.
    """
    return text.strip().lower() in ("true", "false")


def str_is_int(text: str, *, base: int | None = None) -> bool:
    """
    Determine if a string represents an integer value.

    If base is specified as a nonzero value, that number base is used to
    interpret the string. If base is None (default) or zero,
    Python-style prefixes are recognized for binary, octal, and
    hexadecimal values.  If no such prefix is present, the value is
    interpreted as a decimal integer (base 10).
    """
    try:
        _str_to_int(text, base)
    except ValueError:
        return False
    return True


def str_is_float(
        text: str, *, allow_non_finite: bool = True, allow_int: bool = False,
) -> bool:
    """
    Determine if a string represents a float value.

    If allow_non_finite is True (default), special floating-point
    representations such as "-inf", "+inf", and "nan" are recognized as
    float values.  Otherwise, only finite floating-point values are
    recognized.

    If allow_int is False (default), and the string represents a base-10
    integer, then it will not be recognized as a floating-point value.
    Set this option to True if ints should be accepted as floats.
    """
    if not allow_int:
        try:
            int(text)
        except ValueError:
            pass
        else:
            return False
    try:
        value = float(text)
    except ValueError:
        return False
    return allow_non_finite or math.isfinite(value)


def str_type(
        text: str, *, empty_is_none: bool = True, int_base: int | None = None,
        allow_non_finite_float: bool = True
) -> type:
    """
    Infer the basic Python type represented by a string.

    The type is determined by testing for None, bool, int, and float
    values in that order.  Strings that do not represent one of these
    types are inferred as str.

    If empty_is_none is True (default), empty and whitespace-only
    strings are also inferred as NoneType.

    If int_base is specified as a nonzero value, that number base is
    used to interpret the string.  If int_base is None (default) or
    zero, Python-style prefixes are recognized first, and if no prefix
    is present, the value is interpreted as a decimal integer (base 10).

    If allow_non_finite_float is True (default), special floating-point
    representations such as "-inf", "+inf", and "nan" are recognized as
    float values.
    """
    if str_is_none(text, allow_empty=empty_is_none):
        return NoneType
    if str_is_bool(text):
        return bool
    if str_is_int(text, base=int_base):
        return int
    if str_is_float(text, allow_non_finite=allow_non_finite_float):
        return float
    return str


def str_cast(
        text: str, *, empty_is_none: bool = True, int_base: int | None = None,
        allow_non_finite_float: bool = True
) -> bool | int | float | str | None:
    """
    Cast a string to the inferred basic Python type it represents.

    The type is determined by testing for None, bool, int, and float
    values in that order.  Strings that do not represent one of these
    types are returned unchanged as type str.

    If empty_is_none is True (default), empty and whitespace-only
    strings are converted to None.

    If int_base is specified as a nonzero value, that number base is
    used to interpret the string.  If int_base is None (default) or
    zero, Python-style prefixes are recognized first, and if no prefix
    is present, the value is interpreted as a decimal integer (base 10).

    If allow_non_finite_float is True (default), special floating-point
    representations such as "-inf", "+inf", and "nan" are recognized as
    float values.
    """
    if str_is_none(text, allow_empty=empty_is_none):
        return None
    if str_is_bool(text):
        return text.strip().lower() == "true"
    if str_is_int(text, base=int_base):
        return _str_to_int(text, int_base)
    if str_is_float(text, allow_non_finite=allow_non_finite_float):
        return float(text)
    return text


def _validate_not_empty(sep: str, link: str | None = None) -> None:
    """Confirm that conversion string arguments are not empty."""
    if not sep:
        raise ValueError("Argument 'sep' cannot be an empty string.")
    if link is not None and not link:
        raise ValueError("Argument 'link' cannot be an empty string.")


def _get_item_strs(text: str, sep: str, strip: bool) -> Iterator[str]:
    """
    Get an iterator over each string item/entry in the text.

    Parsing depends on the separator and whether to apply stripping.
    """
    split_item_strs = (text.strip() if strip else text).split(sep)
    return (
        item_str.strip() if strip else item_str
        for item_str in split_item_strs
    )


def _str_to_int(text: str, base: int | None) -> int:
    """
    Convert a string to an integer value.

    Raises ValueError if int conversion is not possible for the
    specified text and integer base.
    """
    if base is not None and base != 0:
        return int(text, base)
    try:
        return int(text, 0)
    except ValueError:
        return int(text, 10)
