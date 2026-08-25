"""Test"""


from redsolid.containers import MappingView, SequenceView


def test_mapping_view() -> None:
    """Test"""
    entries = {"a": 1, "b": 2, "c": 3}
    view = MappingView(entries)
    assert len(view) == 3
    assert view["a"] == 1
    assert view.get("b", 4) == 2
    assert view.get("d", 4) == 4
    assert entries.keys() == view.keys()
    assert tuple(entries.values()) == tuple(view.values())
    for key, value in view.items():
        assert entries[key] == value

    entries["d"] = 4
    assert len(view) == 4
    assert view["d"] == 4

    del entries["a"]
    assert len(view) == 3
    assert view.get("a", -1) == -1


def test_sequence_view() -> None:
    """Test"""
    items = [2, 4, 6, 8, 2]
    view = SequenceView(items)
    assert len(view) == 5
    assert view[1] == 4
    assert view.count(2) == 2
    assert view.index(4) == 1
    for index, item in enumerate(view):
        assert items[index] == item

    items.append(10)
    assert len(view) == 6
    assert view[5] == 10

    del items[0]
    assert len(view) == 5
    assert view[0] == 4
