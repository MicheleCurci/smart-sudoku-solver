from sys import int_info
from sudoku_grid_interface import SudokuGridInterface, VectorInterface, CellInterface, SubGridInterface
import itertools


class Vector(VectorInterface):

    def __init__(self, cells: list()) -> None:
        self.cells = cells

    def get_ith(self, i: int) -> CellInterface:
        return self.cells[i]

    def is_valid(self) -> bool:
        for cell in self.cells:
            if not cell.is_valid():
                return False

        values = [cell.get_value()
                  for cell in self.cells if cell.get_value() != 0]
        if len(values) != len(set(values)):
            return False

        return True

    def get_marked_values(self):
        return [cell.get_value() for cell in self.cells if cell.is_marked()]

    def get_unmarked_cells(self):
        return [cell for cell in self.cells if cell.is_empty()]

    # def get_candidates(self) -> set():
    #     candidates = set()
    #     for cell in self.cells:
    #         candidates = candidates.union(cell.get_candidates())
    #     return candidates

    def get_candidates_intersection(self) -> set():
        candidates = set(range(1, 10))
        for cell in self.cells:
            candidates = candidates.intersection(cell.get_candidates())
        return candidates

    def get_candidates_union(self) -> set():
        # candidates = set()
        # for cell in self.cells:
        #     candidates = candidates.union(cell.get_candidates())
        # return candidates
        candidates = [cell.get_candidates() for cell in self.cells]
        if len(candidates) == 0:
            return set()
        return set.union(*candidates)

    def has_candidate(self, candidate):
        for cell in self.cells:
            if cell.has_candidate(candidate):
                return True
        return False

    def difference(self, other: VectorInterface):
        return [cell for cell in self.cells if cell not in other.cells]


class Cell(CellInterface):

    def __init__(self, row: int, column: int, value: int, candidates=set(range(1, 10))) -> None:
        self.row = row
        self.column = column
        self.candidates = candidates
        self.value = 0

        self.set_value(value)

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __repr__(self):
        return "(" + str(self.row) + ", " + str(self.column) + ")"

    def __hash__(self) -> int:
        return hash(str(self.row) + str(self.column) + str(self.candidates))

    def get_position(self) -> tuple:
        return (self.row, self.column)

    def get_value(self) -> int:
        return self.value

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.column

    def set_value(self, value: int) -> None:
        self.value = int(value)
        if self.value in range(1, 10):
            self.candidates = set()

    def is_marked(self) -> bool:
        return self.get_value() in range(1, 10)

    def is_valid(self) -> bool:
        return self.get_value() in range(10)

    def is_empty(self) -> bool:
        return self.get_value() == 0

    def get_candidates(self) -> set():
        return self.candidates

    def has_candidate(self, candidate) -> bool:
        return candidate in self.candidates

    # def has_single_candidate(self) -> bool:
    #     return len(self.candidates) == 1

    def set_candidates(self, candidates: set()) -> None:
        self.candidates = candidates

    def remove_candidate(self, candidate):
        self.candidates.discard(candidate)

    def remove_candidates(self, candidates: set):
        self.candidates = self.candidates.difference(candidates)


class SubGrid(SubGridInterface):

    def __init__(self, subgrid: list(list())) -> None:
        self.grid = subgrid

    def get_cell(self, row: int, col: int) -> CellInterface:
        return self.grid[row][col]

    def is_valid(self) -> bool:
        values = [cell.get_value()
                  for cell in self.flatten() if cell.get_value() != 0]
        if len(values) != len(set(values)):
            return False

        for cell in self.flatten():
            if not cell.is_valid():
                return False
        return True

    def is_filled(self) -> bool:
        values = [cell.get_value() for cell in self.flatten()]
        return values.sort() == list(range(1, 10))

    def flatten(self) -> list:
        cells_in_subgrid = []
        for row in self.grid:
            cells_in_subgrid += row
        return cells_in_subgrid

    def get_all_cells(self) -> list:
        cells_in_subgrid = []
        for row in self.grid:
            cells_in_subgrid += row
        return cells_in_subgrid

    def get_empty_cells(self) -> list:
        cells_in_subgrid = []
        for row in self.grid:
            cells_in_subgrid += row
        return [cell for cell in cells_in_subgrid if cell.is_empty()]

    def get_marked_values(self):
        return [cell.get_value() for cell in self.flatten() if cell.is_marked()]

    def get_other_empty_cells_in_subgrid(self, cells_to_exclude: list):
        return Vector([cell for cell in self.flatten() if cell.is_empty() and cell not in cells_to_exclude])

    def get_rows(self):
        return [Vector(row) for row in self.grid]

    def get_columns(self):
        transposed_grid = list(zip(*self.grid))
        return [Vector(column) for column in transposed_grid]

    def get_empty_rows(self):
        return [Vector(row) for row in self.grid]

    def get_empty_cells_on_columns(self):
        transposed_grid = list(zip(*self.grid))
        return [Vector(column) for column in transposed_grid]


class SudokuGrid(SudokuGridInterface):

    def __init__(self, encoded_sudoku_grid) -> None:

        encoded_sudoku_grid = [int(char)
                               for char in list(encoded_sudoku_grid)[::-1]]
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for column in range(9):
                self.grid[row][column] = Cell(
                    row, column, value=encoded_sudoku_grid.pop())
        self.update_candidates_in_all_cells()

    def __eq__(self, other: SudokuGridInterface) -> bool:
        for row in range(9):
            for column in range(9):
                if self.get_cell(row, column).get_candidates() != other.get_cell(row, column).get_candidates():
                    return False

        return self.decode() == other.decode()

    def is_valid(self) -> bool:
        for row in range(9):
            for column in range(9):
                if not self.get_cell(row, column).is_valid():
                    return False

        for idx in range(9):
            if not self.get_row_ith(self, idx).is_valid():
                return False

            if not self.get_col_ith(self, idx).is_valid():
                return False

            if not self.get_sub_grid(self, idx).is_valid():
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

        excluded_values_from_same_row_column_grid = set(self.get_other_cells_on_column_by_cell(cell).get_marked_values() +
                                                        self.get_other_cells_on_row_by_cell(cell).get_marked_values() +
                                                        self.get_other_cells_in_grid_by_cell(cell).get_marked_values())
        cell.set_candidates(
            cell.get_candidates().difference(excluded_values_from_same_row_column_grid))

    def update_candidates_in_cell_row_column_grid(self, cell):
        cells_to_update = set(list(self.get_other_cells_on_column_by_cell(cell).cells +
                                   self.get_other_cells_on_row_by_cell(cell).cells +
                                   self.get_other_cells_in_grid_by_cell(cell).cells))
        candidate_to_remove = cell.get_value()
        for cell in cells_to_update:
            cell.remove_candidate(candidate_to_remove)

    def get_other_cells_on_row(self, row: int, col: int):
        return Vector([cell for cell in self.grid[row] if cell.get_position() != (row, col)])

    def get_rows(self):
        return [Vector(row) for row in self.grid]

    def get_columns(self):
        transposed_grid = list(zip(*self.grid))
        return [Vector(column) for column in transposed_grid]

    def get_cells_on_row(self, row: int):
        return Vector(self.grid[row])

    def get_empty_cells_on_row(self, row: int):
        return Vector([cell for cell in self.grid[row] if cell.is_empty()])

    def get_other_cells_on_column(self, row: int, col: int):
        return Vector([vector[col] for vector in self.grid if vector[col].get_position() != (row, col)])

    def get_cells_on_column(self, col: int):
        return Vector([row[col] for row in self.grid if row[col].get_col() == col])

    def get_empty_cells_on_col(self, col: int):
        return Vector([row[col] for row in self.grid if row[col].get_col() == col and row[col].is_empty()])

    def get_other_cells_in_grid(self, row: int, col: int):
        return Vector([cell for cell in self.get_sub_grid(
            row, col).flatten() if cell.get_position() != (row, col)])

    def get_other_cells_on_row_by_cell(self, main_cell: Cell):
        return Vector([cell for cell in self.grid[main_cell.get_row()] if cell.get_position() != main_cell.get_position()])

    def get_other_cells_on_column_by_cell(self, main_cell: Cell):
        return Vector([vector[main_cell.get_col()] for vector in self.grid if vector[main_cell.get_col()].get_position() != main_cell.get_position()])

    def get_other_cells_in_grid_by_cell(self, main_cell: Cell):
        return Vector([cell for cell in self.get_sub_grid(
            main_cell.get_row(), main_cell.get_col()).flatten() if cell.get_position() != main_cell.get_position()])

    def get_cell(self, row: int, col: int) -> CellInterface:
        return self.grid[row][col]

    def get_all_cells(self) -> list:
        return [self.get_cell(row, col) for row in range(0, 9) for col in range(0, 9)]

    def get_all_unmarked_cells(self) -> list:
        return [cell for cell in self.get_all_cells() if cell.is_empty()]

    def get_sub_grid(self, row: int, col: int) -> SubGridInterface:
        return SubGrid(subgrid=[rows[col//3*3: col//3*3+3] for rows in self.grid[row//3*3: row//3*3+3]])

    def get_all_sub_grids(self) -> list:
        return [self.get_sub_grid(row, col) for row in range(0, 9, 3) for col in range(0, 9, 3)]

    def set_cell_value(self, cell: Cell, value: int):
        cell.set_value(value)
        self.update_candidates_in_cell_row_column_grid(cell)

    def show(self) -> None:
        grid_draw = '-'*25
        reversed_values = list(self.decode().replace('0', ' '))[:: -1]
        for _ in range(3):  # 3 rows of subgrids
            for _ in range(3):  # 3 rows
                grid_draw += '\n| '
                for _ in range(3):  # 3 horizontal subgrids
                    for _ in range(3):  # 3 inside subgrid
                        grid_draw += reversed_values.pop()
                        grid_draw += ' '
                    grid_draw += '| '
            grid_draw += '\n' + '-'*25
        print(grid_draw)

    def decode(self) -> str:
        decoded_grid = ""
        for row in range(9):
            for column in range(9):
                decoded_grid += str(self.get_cell(row, column).get_value())
        return decoded_grid
