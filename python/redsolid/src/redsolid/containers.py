"""Adapters and read-only views for common collection types."""


from __future__ import annotations
from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
    Set
)
from typing import Any, NoReturn, TypeVar, cast, overload, override


_K = TypeVar("_K")
"""Invariant type variable for a mapping key."""
_T_co = TypeVar("_T_co", covariant=True)
"""Covariant (read-only) type variable for a value."""
_T = TypeVar("_T")
"""Invariant (mutable) type variable for a value."""


class MappingView(Mapping[_K, _T_co]):
    """
    Read-only view over a dict or any other Mapping.

    This class is a wrapper that provides read-only access to the
    mapping itself, preventing entries from being added, changed, or
    removed through the view.  It implements the Mapping interface
    without copying the underlying mapping.

    The wrapper does not make mutable entries immutable.  If the
    underlying mapping is subsequently modified, this wrapper will
    reflect those changes.
    """

    def __init__(self, items: Mapping[_K, _T_co]) -> None:
        """Create read-only view for a mapping of key-value entries."""
        self._items = items

    @override
    def __getitem__(self, key: _K) -> _T_co:
        """Get a value in the mapping based on a key."""
        return self._items[key]

    @override
    def __iter__(self) -> Iterator[_K]:
        """Get an iterator over the keys in the mapping."""
        return iter(self._items)

    @override
    def __len__(self) -> int:
        """Get the number of items in the mapping."""
        return len(self._items)

    @override
    def __repr__(self) -> str:
        """Get a debug string representation."""
        return f"{type(self).__name__}(_items={self._items!r})"

    @override
    def __str__(self) -> str:
        """Get a user string representation."""
        return f"{type(self).__name__}({self._items!r})"


class SequenceView(Sequence[_T_co]):
    """
    Read-only view over a list, tuple, or any other Sequence.

    This class is a wrapper that provides read-only access to the
    sequence itself, preventing items from being added, changed, or
    removed through the view.  It implements the Sequence interface
    without copying the underlying sequence.

    The wrapper does not make mutable items immutable.  If the
    underlying sequence is subsequently modified, this wrapper will
    reflect those changes.
    """

    def __init__(self, items: Sequence[_T_co]) -> None:
        """Create a read-only view for a sequence of items."""
        self._items = items

    @overload
    def __getitem__(self, key: int) -> _T_co:
        ...

    @overload
    def __getitem__(self, key: slice) -> SequenceView[_T_co]:
        ...

    @override
    def __getitem__(self, key: int | slice) -> _T_co | SequenceView[_T_co]:
        """
        Get an item or slice from the sequence based on a key.

        If the key is an index, a single item is returned.  If the key
        is a slice, a new SequenceView is returned that wraps the slice
        items.
        """
        if isinstance(key, slice):
            return SequenceView(self._items[key])
        return self._items[key]

    @override
    def __len__(self) -> int:
        """Get the number of items in the sequence."""
        return len(self._items)

    @override
    def __repr__(self) -> str:
        """Get a debug string representation."""
        return f"{type(self).__name__}(_items={self._items!r})"

    @override
    def __str__(self) -> str:
        """Get a user string representation."""
        return f"{type(self).__name__}({self._items!r})"


class SetView(Set[_T_co]):
    """
    Read-only view over a Set.

    This class is a wrapper that provides read-only access to the set
    itself, preventing items from being added, changed, or removed
    through the view.  It implements the Set interface without copying
    the underlying set.

    The wrapper does not make mutable items immutable.  If the
    underlying set is subsequently modified, this wrapper will reflect
    those changes.
    """

    def __init__(self, items: Set[_T_co]) -> None:
        """Create a read-only view for a set of items."""
        self._items = items

    @override
    def __contains__(self, item: Any) -> bool:
        """Determine if the set contains an item."""
        return item in self._items

    @override
    def __iter__(self) -> Iterator[_T_co]:
        """Get an iterator over the items in the set."""
        return iter(self._items)

    @override
    def __len__(self) -> int:
        """Get the number of items in the set."""
        return len(self._items)

    @override
    def __repr__(self) -> str:
        """Get a debug string representation."""
        return f"{type(self).__name__}(_items={self._items!r})"

    @override
    def __str__(self) -> str:
        """Get a user string representation."""
        return f"{type(self).__name__}({self._items!r})"


class FixedKeysMappingAdapter(MutableMapping[_K, _T]):
    """
    Adapts a dict or other MutableMapping to disallow changes to keys.

    This class is a wrapper that provides both read and write access to
    the values for each key, but it prevents keys from being added or
    removed.  Mutator methods like update, pop, and others will raise a
    TypeError if this is attempted.  It otherwise implements the
    MutableMapping interface without copying the underlying mapping.

    The wrapper does not make mutable values immutable.  If the
    underlying mapping is subsequently modified, this wrapper will
    reflect those changes.
    """

    def __init__(self, items: MutableMapping[_K, _T]) -> None:
        """Create a fixed-keys adapter for a mutable mapping."""
        self._items = items

    @override
    def __delitem__(self, key: _K) -> None:
        """
        Not supported by this class to preserve fixed keys.

        A TypeError is raised if this method is called.
        """
        self._prevent_remove_key(key)

    @override
    def __getitem__(self, key: _K) -> _T:
        """Get a value in the mapping based on a key."""
        return self._items[key]

    @override
    def __iter__(self) -> Iterator[_K]:
        """Get an iterator over the keys in the mapping."""
        return iter(self._items)

    @override
    def __len__(self) -> int:
        """Get the number of entries in the mapping."""
        return len(self._items)

    @override
    def __setitem__(self, key: _K, value: _T) -> None:
        """
        Change the value associated with an existing key.

        To preserve fixed keys, adding a new entry is not supported by
        this class.  A TypeError is raised if this method is called with
        a key that is not currently in the mapping.
        """
        if key not in self._items:
            self._prevent_add_key(key)
        else:
            self._items[key] = value

    @override
    def __repr__(self) -> str:
        """Get a debug string representation."""
        return f"{type(self).__name__}(_items={self._items!r})"

    @override
    def __str__(self) -> str:
        """Get a user string representation."""
        return f"{type(self).__name__}({self._items!r})"

    @override
    def clear(self) -> None:
        """
        Not supported by this class to preserve fixed keys.

        A TypeError is raised if this method is called.
        """
        self._prevent_remove_key()

    @override
    def pop(self, key: _K, default: object = None) -> _T:
        """
        Not supported by this class to preserve fixed keys.

        A TypeError is raised if this method is called.
        """
        self._prevent_remove_key(key)

    @override
    def popitem(self) -> tuple[_K, _T]:
        """
        Not supported by this class to preserve fixed keys.

        A TypeError is raised if this method is called.
        """
        self._prevent_remove_key()

    @override
    def setdefault(self, key: _K, default: object = None) -> _T:
        """
        Get the value associated with an existing key.

        To preserve fixed keys, adding a new entry is not supported by
        this class.  If the key exists, its associated value is returned
        and default is ignored.  A TypeError is raised if this method is
        called with a key that is not currently in the mapping.
        """
        if key not in self._items:
            self._prevent_add_key(key)
        return self._items[key]

    @override
    # Lint: Mypy omits the runtime kwargs parameter in update method.
    def update(  # type: ignore[override]
            self, other: Mapping[_K, _T] | Iterable[tuple[_K, _T]] = (),
            /, **kwargs: _T
    ) -> None:
        """
        Update values associated with existing keys.

        To preserve fixed keys, adding new entries is not supported by
        this class.  A TypeError is raised if this method is called with
        one or more keys that are not currently in the mapping.  Keyword
        arguments are treated as key/value pairs, but each key must
        already exist in the mapping.
        """
        other_dict = dict(other)
        other_new_keys = other_dict.keys() - self._items.keys()
        if other_new_keys:
            self._prevent_add_key(next(iter(other_new_keys)))
        for kwargs_key in kwargs:
            if kwargs_key not in self._items:
                self._prevent_add_key(cast(_K, kwargs_key))
        self._items.update(other_dict)
        for kwargs_key, kwargs_value in kwargs.items():
            self._items[cast(_K, kwargs_key)] = kwargs_value

    def _prevent_add_key(self, key: _K) -> NoReturn:
        """Raise TypeError if an attempt was made to add a key."""
        raise TypeError(
            f"Adapter does not support adding new keys (key={key!r})."
        )

    def _prevent_remove_key(self, key: _K | None = None) -> NoReturn:
        """Raise TypeError if an attempt was made to remove a key."""
        key_text = "" if key is None else f" (key={key!r})"
        raise TypeError(
            f"Adapter does not support removing existing keys{key_text}."
        )


class FixedLengthSequenceAdapter(MutableSequence[_T]):
    """
    Adapts a MutableSequence to disallow changes in length.

    This class is a wrapper that provides both read and write access to
    the items, but it does not allow the sequence to increase or
    decrease in length.  Mutator methods like insert, remove, and others
    will raise a TypeError if this is attempted.  It otherwise
    implements the MutableSequence interface without copying the
    underlying sequence.

    The wrapper does not make mutable items immutable.  If the
    underlying sequence is subsequently modified, this wrapper will
    reflect those changes.
    """

    def __init__(self, items: MutableSequence[_T]) -> None:
        """Create a fixed-length adapter for a mutable sequence."""
        self._items = items

    @overload
    def __delitem__(self, key: int) -> None:
        ...

    @overload
    def __delitem__(self, key: slice) -> None:
        ...

    @override
    def __delitem__(self, key: int | slice) -> None:
        """
        Not supported by this class to preserve fixed length.

        A TypeError is raised if this method is called.
        """
        self._prevent_remove_item(key)

    @overload
    def __getitem__(self, key: int) -> _T:
        ...

    @overload
    def __getitem__(self, key: slice) -> MutableSequence[_T]:
        ...

    @override
    def __getitem__(self, key: int | slice) -> _T | MutableSequence[_T]:
        """Lookup one or more items by index or slice."""
        return self._items[key]

    @override
    def __iter__(self) -> Iterator[_T]:
        """Get an iterator over the items in the sequence."""
        return iter(self._items)

    @override
    def __len__(self) -> int:
        """Get the number of items in the sequence."""
        return len(self._items)

    @overload
    def __setitem__(self, key: int, value: _T) -> None:
        ...

    @overload
    def __setitem__(self, key: slice, value: Iterable[_T]) -> None:
        ...

    @override
    def __setitem__(self, key: int | slice, value: _T | Iterable[_T]) -> None:
        """
        Replace one or more items by index or slice.

        If the key is an index, a single item is replaced.  If the key
        is a slice, the replacement must contain exactly the same number
        of items that the slice selects.

        To preserve fixed length, adding or removing items is not
        supported by this class.  A TypeError is raised if this method
        is called with an index or slice that would change the length
        of the sequence.
        """
        if isinstance(key, int):
            self._items[key] = cast(_T, value)
            return
        start, stop, step = key.indices(len(self._items))
        selected_length = len(range(start, stop, step))
        values = tuple(cast(Iterable[_T], value))
        if len(values) > selected_length:
            self._prevent_add_item(start)
        elif len(values) < selected_length:
            self._prevent_remove_item(start)
        self._items[key] = values

    @override
    def __repr__(self) -> str:
        """Get a debug string representation."""
        return f"{type(self).__name__}(_items={self._items!r})"

    @override
    def __str__(self) -> str:
        """Get a user string representation."""
        return f"{type(self).__name__}({self._items!r})"

    @override
    def insert(self, index: int, value: _T) -> None:
        """
        Not supported by this class to preserve fixed length.

        A TypeError is raised if this method is called.
        """
        self._prevent_add_item(index)

    def _prevent_add_item(self, index: int) -> NoReturn:
        """Raise TypeError if an attempt was made to add an item."""
        raise TypeError(
            f"Adapter does not support adding new items (index={index!r})."
        )

    def _prevent_remove_item(self, key: int | slice) -> NoReturn:
        """Raise TypeError if an attempt was made to remove an item."""
        key_text = "index" if isinstance(key, int) else "slice"
        raise TypeError(
            "Adapter does not support removing existing items without "
            f"replacement ({key_text}={key!r})."
        )


class FixedSizeGrid(SequenceView[FixedLengthSequenceAdapter[_T]]):
    """
    Represents a 2-D grid of cells with a value for each cell.

    The grid has specified dimensions (width and height) that cannot be
    changed.  At creation, each cell has a specified initial default
    value.  The value for each cell can be changed as needed after
    creation.
    """

    CellOffset = tuple[int, int]
    """Type hint for a grid cell offset as an (x, y) tuple."""

    def __init__(self, width: int, height: int, default_value: _T) -> None:
        """
        Initialize grid dimensions and default value.

        Width and height must be positive integers.  If the default
        value is mutable, the same object reference is assigned to every
        cell (not copied).
        """
        if width <= 0:
            raise ValueError("Argument 'width' must be greater than zero.")
        if height <= 0:
            raise ValueError("Argument 'height' must be greater than zero.")
        rows = [
            FixedLengthSequenceAdapter[_T]([default_value] * width)
            for _ in range(height)
        ]
        super().__init__(rows)
        self._width = width
        self._height = height
        self._default_value = default_value

    @overload
    def __getitem__(self, key: int) -> FixedLengthSequenceAdapter[_T]:
        ...

    @overload
    def __getitem__(
            self, key: slice
    ) -> SequenceView[FixedLengthSequenceAdapter[_T]]:
        ...

    @overload
    def __getitem__(self, key: CellOffset) -> _T:
        ...

    @override
    def __getitem__(
            self, key: int | slice | CellOffset
    ) -> (
            _T
            | FixedLengthSequenceAdapter[_T]
            | SequenceView[FixedLengthSequenceAdapter[_T]]
    ):
        """
        Get one or more rows or a single cell value from the grid.

        If the key is an (x, y) offset, the value of the cell at that
        location is returned.  If the key is a singular index, the row
        at that index is returned.  Multiple rows can be returned if the
        key uses slice notation.

        Note that grid[y][x] == grid[x, y].  The first notation is
        consistent with the row-major grid structure, while the second
        notation is consistent with more standard x-first conventions.
        """
        if isinstance(key, tuple):
            x, y = key
            return super().__getitem__(y)[x]
        return super().__getitem__(key)

    def __setitem__(self, key: CellOffset, value: _T) -> None:
        """
        Set a cell value in the grid based on its x, y offset.

        Note that grid[y][x] == grid[x, y].  The first notation is
        consistent with the row-major grid structure, while the second
        notation is consistent with more standard x-first conventions.
        """
        x, y = key
        super().__getitem__(y)[x] = value

    @override
    def __repr__(self) -> str:
        """Get a debug string representation."""
        return (
            f"{type(self).__name__}(width={self.width!r}, "
            f"height={self.height!r}, _default_value={self._default_value!r})"
        )

    @override
    def __str__(self) -> str:
        """Get a user string representation."""
        return f"{type(self).__name__}({self.width} x {self.height})"

    @property
    def width(self) -> int:
        """Get the x dimension (width) of the grid."""
        return self._width

    @property
    def height(self) -> int:
        """Get the y dimension (height) of the grid."""
        return self._height

    @property
    def default_value(self) -> _T:
        """Get value assigned to cells when the grid is initialized."""
        return self._default_value

    @property
    def cell_count(self) -> int:
        """Get the number of cells (width * height) in the grid."""
        return self._width * self._height

    @property
    def dimensions(self) -> tuple[int, int]:
        """Get the width and height dimensions as a tuple."""
        return (self._width, self._height)

    def offsets(self) -> Iterator[CellOffset]:
        """
        Get an iterator over all cell offsets in the grid.

        The iterator yields (x, y) tuples.  Cells are traversed
        in row-major order, with x incremented before y.
        """
        for y in range(self._height):
            for x in range(self._width):
                yield (x, y)

    def cells(self) -> Iterator[tuple[int, int, _T]]:
        """
        Get an iterator over all cells in the grid.

        The iterator yields (x, y, value) tuples.  Cells are traversed
        in row-major order, with x incremented before y.
        """
        for y, row in enumerate(self):
            for x, value in enumerate(row):
                yield (x, y, value)

    def get_unique_values(self) -> set[_T]:
        """
        Get the set of distinct cell values in the grid.

        Cell values must be hashable in order to get unique values.
        A TypeError is raised if a value in the grid is not hashable.
        """
        return {value for _, _, value in self.cells()}

    def find_all(self, value: _T) -> Iterator[CellOffset]:
        """
        Get an iterator over all (x, y) offsets with the given value.

        The iterator yields (x, y) tuples for every cell that has the
        specified value.
        """
        for x, y, search_value in self.cells():
            if search_value == value:
                yield (x, y)

    def set_all(
            self, value: _T, offsets: Iterable[CellOffset] | None = None
    ) -> None:
        """Set cells at specified (x, y) offsets to the same value."""
        selected_offsets = offsets if offsets is not None else self.offsets()
        for x, y in selected_offsets:
            self[x, y] = value

    def clear_cell(self, x: int, y: int) -> None:
        """Set cell at specified (x, y) offset to the default value."""
        self[x, y] = self._default_value

    def clear_all(self, offsets: Iterable[CellOffset] | None = None) -> None:
        """Set cells at specified (x, y) offsets to default value."""
        selected_offsets = offsets if offsets is not None else self.offsets()
        for x, y in selected_offsets:
            self[x, y] = self._default_value
