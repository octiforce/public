# RedSolid

Reusable Python libraries, utilities, and tools for software development.

RedSolid is a collection of general-purpose Python components intended to
be reusable across software projects.

## Requirements

- Python 3.12 or later

## Installation

Install RedSolid from PyPI:

```console
python -m pip install redsolid
```

## Available Modules
### `redsolid.containers`

Provides collection classes, views, and adapters for working with Python
collections.

Components include:

- `SequenceView` - read-only view over a sequence
- `MappingView` - read-only view over a mapping
- `SetView` - read-only view over a set
- `FixedLengthSequenceAdapter` - mutable sequence adapter with fixed length
- `FixedKeysMappingAdapter` - mutable mapping adapter with fixed keys
- `FixedSizeGrid` - fixed-size two-dimensional grid

### `redsolid.strings`

Provides string conversion and utility functions for common software
development tasks.

Components include:

- `Indent` - indent strings and track indentation level for nested output
- `str_from_*` - convert a sequence or mapping to a structured string
- `str_to_*` - convert a string to a list, tuple, set, or dict
- `str_is_*` - determine if a string represents a value of a basic type
- `str_type` - infer the basic Python type associated with a string
- `str_cast` - cast string to the inferred basic Python type it represents

## Development

Clone the repository and install RedSolid in editable mode with its
development dependencies:

```console
python -m pip install --group dev -e .
```

Run the test suite:

```console
python -m pytest
```

Run the static type checker:

```console
mypy --strict src/redsolid tests
```

Run pyright:

```console
pyright
```

Run the linting tools:

```console
pycodestyle src/redsolid tests
pydocstyle src/redsolid tests
pylint src/redsolid tests
ruff check src/redsolid tests
```

## License

RedSolid is distributed under the MIT License.

## Repository

RedSolid source code is maintained at:

https://github.com/octiforce/public/tree/main/python/redsolid
