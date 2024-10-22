from typing import Self
from src.sudoku.cell import Cell
from src.sudoku.cells_set import CellsSet
from src.sudoku_entities import Square


class Grid():
    def __init__(self, encoded_sudoku_grid) -> None:
        if isinstance(encoded_sudoku_grid, str):
            encoded_sudoku_grid = [
                int(char) for char in list(encoded_sudoku_grid)[::-1]
            ]
        elif isinstance(encoded_sudoku_grid, list):
            encoded_sudoku_grid = [
                int(value) for chunk in encoded_sudoku_grid for value in chunk
            ][::-1]
        self.grid = [[Cell(0, 0, 0) for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for column in range(9):
                self.grid[row][column] = Cell(
                    row, column, value=encoded_sudoku_grid.pop()
                )
        self.update_candidates_in_all_cells()

    def __eq__(self, other: Self) -> bool:
        for row in range(9):
            for column in range(9):
                if (self.get_cell(row, column).get_candidates() != other.get_cell(row, column).get_candidates()) \
                    or (self.get_cell(row, column).get_value() != other.get_cell(row, column).get_value()):
                    return False
        return True

    def is_valid(self) -> bool:
        for row in self.get_rows():
            if not row.is_valid():
                return False

        for col in self.get_columns():
            if not col.is_valid():
                return False

        for square in self.get_all_squares():
            if not square.is_valid():
                return False

        return True

    def is_filled(self) -> bool:
        for row in range(9):
            for column in range(9):
                if not self.get_cell(row, column).get_value() in range(1, 10):
                    return False

        return True

    def update_candidates_in_all_cells(self):
        for cell in self.get_all_cells():
            self.update_candidates_in_cell(cell)

    def update_candidates_in_cell(self, cell: Cell):
        if cell.is_marked():
            return

        excluded_values_from_same_row_column_grid = set(
            self.get_other_cells_on_column_by_cell(cell).get_marked_values()
            + self.get_other_cells_on_row_by_cell(cell).get_marked_values()
            + self.get_other_cells_in_grid_by_cell(cell).get_marked_values()
        )
        cell.set_candidates(
            cell.get_candidates().difference(excluded_values_from_same_row_column_grid)
        )

    def update_candidates_in_cell_row_column_grid(self, cell):
        cells_to_update = set(
            list(self.get_other_cells_on_column_by_cell(cell).get_cells())
            + list(self.get_other_cells_on_row_by_cell(cell).get_cells())
            + list(self.get_other_cells_in_grid_by_cell(cell).get_cells())
        )
        candidate_to_remove = cell.get_value()
        for cell_to_update in cells_to_update:
            cell_to_update.remove_candidate(candidate_to_remove)

    def get_other_cells_on_row(self, row: int, col: int):
        return CellsSet(
            {cell for cell in self.grid[row] if cell.get_position() != (row, col)}
        )

    def get_rows(self):
        return [CellsSet(set(row)) for row in self.grid]

    def get_columns(self):
        transposed_grid = list(zip(*self.grid))
        return [CellsSet(column) for column in transposed_grid]

    # def get_cells_on_row(self, row: int):
    #     return CellsSet(self.grid[row])

    def get_empty_cells_on_row(self, row: int):
        return CellsSet({cell for cell in self.grid[row] if cell.is_empty()})

    def get_other_cells_on_column(self, row: int, col: int):
        return CellsSet(
            {
                vector[col]
                for vector in self.grid
                if vector[col].get_position() != (row, col)
            }
        )

    # def get_cells_on_column(self, col: int):
    #     return CellsSet([row[col] for row in self.grid if row[col].get_col() == col])

    def get_empty_cells_on_col(self, col: int):
        return CellsSet(
            {
                row[col]
                for row in self.grid
                if row[col].get_col() == col and row[col].is_empty()
            }
        )

    def get_other_cells_in_grid(self, row: int, col: int):
        return CellsSet(
            {
                cell
                for cell in self.get_square(row, col).flatten()
                if cell.get_position() != (row, col)
            }
        )

    def get_other_cells_on_row_by_cell(self, main_cell: Cell):
        return CellsSet(
            {
                cell
                for cell in self.grid[main_cell.get_row()]
                if cell.get_position() != main_cell.get_position()
            }
        )

    def get_other_cells_on_column_by_cell(self, main_cell: Cell):
        return CellsSet(
            {
                vector[main_cell.get_col()]
                for vector in self.grid
                if vector[main_cell.get_col()].get_position()
                != main_cell.get_position()
            }
        )

    def get_other_cells_in_grid_by_cell(self, main_cell: Cell):
        return CellsSet(
            {
                cell
                for cell in self.get_square(
                    main_cell.get_row(), main_cell.get_col()
                ).flatten()
                if cell.get_position() != main_cell.get_position()
            }
        )

    def get_cell(self, row: int, col: int) -> Cell:
        return self.grid[row][col]

    def get_all_cells(self) -> list:
        return [self.get_cell(row, col) for row in range(0, 9) for col in range(0, 9)]

    # def get_all_unmarked_cells(self) -> list:
    #     return [cell for cell in self.get_all_cells() if cell.is_empty()]

    def get_square(self, row: int, col: int) -> Square:
        return Square(
            square=[
                rows[col // 3 * 3 : col // 3 * 3 + 3]
                for rows in self.grid[row // 3 * 3 : row // 3 * 3 + 3]
            ]
        )

    def get_all_squares(self) -> list[Square]:
        return [
            self.get_square(row, col)
            for row in range(0, 9, 3)
            for col in range(0, 9, 3)
        ]

    def set_cell_value(self, cell: Cell, value: int):
        cell.set_value(value)
        self.update_candidates_in_cell_row_column_grid(cell)

    def show(self) -> None:
        grid_draw = "-" * 25
        reversed_values = list(self.encode().replace("0", " "))[::-1]
        for _ in range(3):  # 3 rows of squares
            for _ in range(3):  # 3 rows
                grid_draw += "\n| "
                for _ in range(3):  # 3 horizontal squares
                    for _ in range(3):  # 3 inside square
                        grid_draw += reversed_values.pop()
                        grid_draw += " "
                    grid_draw += "| "
            grid_draw += "\n" + "-" * 25
        print(grid_draw)

    def encode(self) -> str:
        encoded_grid = ""
        for row in range(9):
            for column in range(9):
                encoded_grid += str(self.get_cell(row, column).get_value())
        return encoded_grid