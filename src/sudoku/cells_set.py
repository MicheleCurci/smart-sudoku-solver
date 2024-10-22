import itertools
from typing import Self
from src.sudoku.cell import Cell


class CellsSet:
    def __init__(self, cells) -> None:
        self.cells = set(cells)

    def __iter__(self):
        return iter(self.cells)

    def get_cells(self) -> set[Cell]:
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

    # def get_candidates(self) -> set():
    #     candidates = set()
    #     for cell in self.cells:
    #         candidates = candidates.union(cell.get_candidates())
    #     return candidates

    # def get_candidates_intersection(self) -> set():
    #     candidates_for_each_cell = [cell.get_candidates()
    #                                 for cell in self.cells]
    #     if candidates_for_each_cell == []:
    #         return set()
    #     return set.intersection(*candidates_for_each_cell)

    def get_candidates_union(self) -> set[int]:
        candidates_for_each_cell = [cell.get_candidates() for cell in self.get_cells()]
        if candidates_for_each_cell == []:
            return set()
        return set.union(*candidates_for_each_cell)

    # def has_candidate(self, candidate):
    #     for cell in self.cells:
    #         if cell.has_candidate(candidate):
    #             return True
    #     return False

    # def union(self, other: AbstractCellsSet):
    #     tt = other.get_candidates_union()
    #     return CellsSet(self.cells.union(tt))

    def difference(self, other: Self):
        return CellsSet(self.get_cells().difference(other.get_cells()))


########## FROM SQUARE

    # def is_filled(self) -> bool:
    #     values = [cell.get_value() for cell in self.flatten()]
    #     return values.sort() == list(range(1, 10))

    # TODO: remove
    def flatten(self) -> list[Cell]:
        return list(self.cells)

    # def get_all_cells(self) -> list:
    #     cells_in_square = []
    #     for row in self.grid:
    #         cells_in_square += row
    #     return cells_in_square

    def get_other_empty_cells_in_square(self, cells_to_exclude: list):
        return CellsSet(
            {
                cell
                for cell in self.flatten()
                if cell.is_empty() and cell not in cells_to_exclude
            }
        )

    def get_rows(self):
        return [CellsSet(set(row)) for key, row in itertools.groupby(self.cells, lambda x: x.get_row())]

    def get_columns(self):
        return [CellsSet(set(row)) for key, row in itertools.groupby(self.cells, lambda x: x.get_col())]


    # def get_empty_rows(self):
    #     return [CellsSet(row) for row in self.grid]

    # def get_empty_cells_on_columns(self):
    #     transposed_grid = list(zip(*self.grid))
    #     return [CellsSet(column) for column in transposed_grid]

