import pytest
from src.sudoku.cell import Cell


def test_init():
    cell = Cell(1, 2, 5)
    assert cell.get_row() == 1
    assert cell.get_col() == 2
    assert cell.get_value() == 5
    assert cell.get_candidates() == set()


def test_set_value():
    cell = Cell(1, 2, 0)
    cell.set_value(3)
    assert cell.get_value() == 3
    assert cell.get_candidates() == set()


def test_is_marked():
    cell = Cell(1, 2, 3)
    assert cell.is_marked() is True
    cell.set_value(0)
    assert cell.is_marked() is False


def test_is_empty():
    cell = Cell(1, 2, 0)
    assert cell.is_empty() is True
    cell.set_value(3)
    assert cell.is_empty() is False


def test_is_valid():
    cell = Cell(1, 2, 5)
    assert cell.is_valid() is True
    cell.set_value(10)
    assert cell.is_valid() is False


def test_add_and_remove_candidates():
    cell = Cell(1, 2, 0)
    cell.set_candidates({1, 2, 3})
    assert cell.get_candidates() == {1, 2, 3}
    cell.remove_candidate(2)
    assert cell.get_candidates() == {1, 3}
    cell.remove_candidates({1, 3})
    assert cell.get_candidates() == set()


def test_eq():
    cell1 = Cell(1, 2, 3)
    cell2 = Cell(1, 2, 4)
    assert cell1 == cell2


def test_hash():
    cell1 = Cell(1, 2, 3)
    cell2 = Cell(1, 2, 4)
    assert hash(cell1) == hash(cell2)


def test_repr():
    cell = Cell(1, 2, 3)
    assert repr(cell) == "(1, 2)"
