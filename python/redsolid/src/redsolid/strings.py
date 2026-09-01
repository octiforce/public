"""String transformation and formatting solutions."""


from __future__ import annotations

from collections.abc import Callable, Generator, Iterable, Iterator, Mapping
from contextlib import contextmanager
from typing import Any, override


class Indenter:
    """
    Indents strings and tracks indentation level for nested output.

    Indenters can use separate step text for continuing and ending
    indentation (both step types are 4 spaces by default).  The push()
    and pop() methods add or remove one or more indent levels.  The
    indent() method returns a string prefixed with the indentation
    steps.
    """

    @staticmethod
    def _validate_not_empty(name: str, value: str) -> None:
        """Confirm that argument is not an empty string."""
        if not value:
            raise ValueError(f"Argument {name!r} cannot be an empty string.")

    @staticmethod
    def _validate_positive(name: str, value: int) -> None:
        """Confirm that argument is greater than zero."""
        if value <= 0:
            raise ValueError(f"Argument {name!r} must be greater than zero.")

    def __init__(
            self, *, continue_step: str = "    ", end_step: str = "    "
    ) -> None:
        """Initialize the indenter."""
        self._validate_not_empty("continue_step", continue_step)
        self._validate_not_empty("end_step", end_step)
        self._continue_step = continue_step
        self._end_step = end_step
        self._steps: list[str] = []
        self._prefix = ""

    @override
    def __repr__(self) -> str:
        """Get a debug string representation."""
        return (
            f"{type(self).__name__}(continue_step={self._continue_step!r}, "
            f"end_step={self.end_step!r}, steps={self.steps!r}, "
            f"prefix={self.prefix!r})"
        )

    @override
    def __str__(self) -> str:
        """Get a user string representation."""
        return self._prefix

    @property
    def continue_step(self) -> str:
        """Get the step text used for continuing indentation."""
        return self._continue_step

    @property
    def end_step(self) -> str:
        """Get the default step text used for ending indentation."""
        return self._end_step

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
        """Get the combined text of the current indentation steps."""
        return self._prefix

    def push(
            self, *, step_count: int = 1, custom_step: str | None = None
    ) -> None:
        """
        Increase (push) the indentation level by one or more steps.

        By default, the indentation is increased by one step using the
        default end step text.  If a custom step is specified, it is
        applied to the new level(s), and the custom text persists until
        those levels are popped.
        """
        self._validate_positive("step_count", step_count)
        if custom_step is not None:
            self._validate_not_empty("custom_step", custom_step)
        continue_step = (
            self._continue_step if custom_step is None else custom_step
        )
        end_step = self._end_step if custom_step is None else custom_step
        self._steps.extend([continue_step] * (step_count - 1))
        self._steps.append(end_step)
        self._prefix = "".join(self._steps)

    def pop(self, *, step_count: int = 1) -> None:
        """
        Decrease (pop) the indentation level by one or more steps.

        By default, the indentation is decreased by one step.  Raises
        ValueError if step_count exceeds the current indentation level.
        """
        self._validate_positive("step_count", step_count)
        if step_count > self.level:
            raise ValueError(
                f"Attempted to pop {step_count} indent step(s), but current "
                f"indent level ({self.level}) is too low."
            )
        del self._steps[-step_count:]
        self._prefix = "".join(self._steps)

    def indent(self, value: object) -> str:
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
    def pushed(
            self, *, step_count: int = 1, custom_step: str | None = None
    ) -> Generator[Indenter, None, None]:
        """
        Temporarily increase the indentation level by one or more steps.

        This method is a context manager for use with the 'with'
        statement.  The previous indentation level is automatically
        restored when the context is exited, including if an exception
        occurs.

        By default, the indentation is increased by one step using the
        default end step text.  If a custom step is specified, it is
        applied to the new level(s), and the custom text persists until
        those levels are popped.
        """
        self.push(step_count=step_count, custom_step=custom_step)
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
    _validate_sep_arg(sep)
    return sep.join(str(item) for item in items)


def str_to_list(
        text: str, *, sep: str = "\n",
        converter: Callable[[str], Any] = str, strip: bool = True
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
    _validate_sep_arg(sep)
    item_strs = _get_item_strs(text, sep, strip)
    items: list[Any] = []
    for item_str in item_strs:
        if item_str != "" or not strip:
            items.append(converter(item_str))
    return items


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
    _validate_sep_arg(sep)
    _validate_link_arg(link)
    return sep.join(f"{key}{link}{value}" for key, value in items.items())


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
    _validate_sep_arg(sep)
    _validate_link_arg(link)
    item_strs = _get_item_strs(text, sep, strip)
    items: dict[Any, Any] = {}
    for item_str in item_strs:
        if not item_str and strip:
            continue
        _validate_contains_link(link, item_str)
        link_index = item_str.find(link)
        key_str = item_str[:link_index]
        value_str = item_str[link_index + len(link):]
        if strip:
            key_str = key_str.strip()
            value_str = value_str.strip()
        key = key_converter(key_str)
        items[key] = value_converter(value_str)
    return items


def _validate_sep_arg(value: str) -> None:
    """Confirm that conversion argument 'sep' is valid."""
    if not value:
        raise ValueError("Argument 'sep' cannot be an empty string.")


def _validate_link_arg(value: str) -> None:
    """Confirm that conversion argument 'link' is valid."""
    if not value:
        raise ValueError("Argument 'link' cannot be an empty string.")


def _validate_contains_link(link: str, value: str) -> None:
    """Confirm that mapping entry contains the specified link string."""
    if link not in value:
        raise ValueError(
            f"Entry {value!r} does not contain link string {link!r}."
        )


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
