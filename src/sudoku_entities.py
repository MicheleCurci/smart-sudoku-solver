from __future__ import annotations
from src.abstract_sudoku_classes import AbstractSquare
from src.sudoku.cell import Cell
from src.sudoku.cells_set import CellsSet



class Square(AbstractSquare):
    def __init__(self, square: list[list[Cell]]) -> None:
        self.grid = square

    # def get_cell(self, row: int, col: int) -> AbstractCell:
    #     return self.grid[row][col]

    def is_valid(self) -> bool:
        return set(self.get_marked_values()) == set(range(1, 10))

    # def is_filled(self) -> bool:
    #     values = [cell.get_value() for cell in self.flatten()]
    #     return values.sort() == list(range(1, 10))

    def flatten(self) -> list[Cell]:
        cells_in_square: list[Cell] = []
        for row in self.grid:
            cells_in_square += row
        return cells_in_square

    # def get_all_cells(self) -> list:
    #     cells_in_square = []
    #     for row in self.grid:
    #         cells_in_square += row
    #     return cells_in_square

    def get_empty_cells(self) -> list:
        cells_in_square: list[Cell] = []
        for row in self.grid:
            cells_in_square += row
        return [cell for cell in cells_in_square if cell.is_empty()]

    def get_marked_values(self):
        return [cell.get_value() for cell in self.flatten() if cell.is_marked()]

    def get_other_empty_cells_in_square(self, cells_to_exclude: list):
        return CellsSet(
            {
                cell
                for cell in self.flatten()
                if cell.is_empty() and cell not in cells_to_exclude
            }
        )

    def get_rows(self):
        return [CellsSet(set(row)) for row in self.grid]

    def get_columns(self):
        transposed_grid = list(zip(*self.grid))
        return [CellsSet(column) for column in transposed_grid]

    # def get_empty_rows(self):
    #     return [CellsSet(row) for row in self.grid]

    # def get_empty_cells_on_columns(self):
    #     transposed_grid = list(zip(*self.grid))
    #     return [CellsSet(column) for column in transposed_grid]

