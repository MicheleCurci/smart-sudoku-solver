import itertools
from typing import Self, TypeAlias
from src.sudoku.cell import Cell

CellsSet: TypeAlias = set[Cell]

# A group can represent one of the following:
# - Row
# - Column
# - Square (3x3)

class CellsGroup:
    def __init__(self, cells) -> None:
        self.cells: CellsSet = set(cells)

    def __iter__(self):
        return iter(self.cells)

    def get_cells(self) -> CellsSet:
        return self.cells

    def is_valid(self) -> bool:
        return set(self.get_marked_values()) == set(range(1, 10))

    def is_empty(self) -> bool:
        return len(self.cells) == 0

    # TODO: random? Why need this?
    # return random cell
    def get_cell(self) -> Cell:
        return list(self.cells)[0]

    def get_marked_values(self):
        return [cell.get_value() for cell in self.get_cells() if cell.is_marked()]

    def get_empty_cells(self):
        return [cell for cell in self.get_cells() if cell.is_empty()]

    def get_candidates_union(self) -> set[int]:
        candidates_for_each_cell = [cell.get_candidates() for cell in self.get_cells()]
        if candidates_for_each_cell == []:
            return set()
        return set.union(*candidates_for_each_cell)

    def difference(self, other: Self):
        return CellsGroup(self.get_cells().difference(other.get_cells()))

    def get_rows(self):
        return [CellsGroup(set(row)) for _, row in itertools.groupby(self.cells, lambda x: x.get_row())]

    def get_columns(self):
        return [CellsGroup(set(col)) for _, col in itertools.groupby(self.cells, lambda x: x.get_col())]

#### SQUARE methods

    def get_other_empty_cells_in_square(self, cells_to_exclude: CellsSet):
        return CellsGroup(
            {
                cell
                for cell in self.cells
                if cell.is_empty() and cell not in cells_to_exclude
            }
        )
