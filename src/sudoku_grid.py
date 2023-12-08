from sys import int_info
from sudoku_grid_interface import GridInterface, CellGroupInterface, CellInterface, SquareInterface
# from typeguard import typechecked


class CellGroup(CellGroupInterface):

    def __init__(self, cells: set) -> None:
        self.cells = set(cells)

    def __iter__(self):
        return iter(self.cells)
    
    def get_cells(self):
        return self.cells

    def is_valid(self) -> bool:
        return all([cell.is_valid() for cell in self.cells]) and self.cells == set(range(1, 10))

    def is_empty(self) -> bool:
        return len(self.cells) == 0

    # return random cell
    def get_cell(self) -> CellInterface:
        return list(self.cells)[0]

    def get_marked_values(self):
        return [cell.get_value() for cell in self.cells if cell.is_marked()]

    def get_empty_cells(self):
        return [cell for cell in self.cells if cell.is_empty()]

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

    def get_candidates_union(self) -> set:
        candidates_for_each_cell = [cell.get_candidates()
                                    for cell in self.cells]
        if candidates_for_each_cell == []:
            return set()
        return set.union(*candidates_for_each_cell)

    # def has_candidate(self, candidate):
    #     for cell in self.cells:
    #         if cell.has_candidate(candidate):
    #             return True
    #     return False

    # def union(self, other: CellGroupInterface):
    #     tt = other.get_candidates_union()
    #     return CellGroup(self.cells.union(tt))

    def difference(self, other: CellGroupInterface):
        return CellGroup(self.cells.difference(other.cells))


class Cell(CellInterface):

    def __init__(self, row: int, column: int, value: int, candidates:set =set(range(1, 10))) -> None:
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

    def get_candidates(self) -> set:
        return self.candidates

    # def has_candidate(self, candidate) -> bool:
    #     return candidate in self.candidates

    # def has_single_candidate(self) -> bool:
    #     return len(self.candidates) == 1

    def set_candidates(self, candidates: set) -> None:
        self.candidates = candidates

    def remove_candidate(self, candidate):
        self.candidates.discard(candidate)

    def remove_candidates(self, candidates: set):
        self.candidates = self.candidates.difference(candidates)


class Square(SquareInterface):

    def __init__(self, square: set[set]) -> None:
        self.grid = square

    # def get_cell(self, row: int, col: int) -> CellInterface:
    #     return self.grid[row][col]

    def is_valid(self) -> bool:
        values = [cell.get_value()
                  for cell in self.flatten() if cell.get_value() != 0]
        if len(values) != len(set(values)):
            return False

        for cell in self.flatten():
            if not cell.is_valid():
                return False
        return True

    # def is_filled(self) -> bool:
    #     values = [cell.get_value() for cell in self.flatten()]
    #     return values.sort() == list(range(1, 10))

    def flatten(self) -> list:
        cells_in_square = []
        for row in self.grid:
            cells_in_square += row
        return cells_in_square

    # def get_all_cells(self) -> list:
    #     cells_in_square = []
    #     for row in self.grid:
    #         cells_in_square += row
    #     return cells_in_square

    def get_empty_cells(self) -> list:
        cells_in_square = []
        for row in self.grid:
            cells_in_square += row
        return [cell for cell in cells_in_square if cell.is_empty()]

    # def get_marked_values(self):
    #     return [cell.get_value() for cell in self.flatten() if cell.is_marked()]

    def get_other_empty_cells_in_square(self, cells_to_exclude: list):
        return CellGroup({cell for cell in self.flatten() if cell.is_empty() and cell not in cells_to_exclude})

    def get_rows(self):
        return [CellGroup(row) for row in self.grid]

    def get_columns(self):
        transposed_grid = list(zip(*self.grid))
        return [CellGroup(column) for column in transposed_grid]

    # def get_empty_rows(self):
    #     return [CellGroup(row) for row in self.grid]

    # def get_empty_cells_on_columns(self):
    #     transposed_grid = list(zip(*self.grid))
    #     return [CellGroup(column) for column in transposed_grid]


class Grid(GridInterface):

    def __init__(self, encoded_sudoku_grid) -> None:

        encoded_sudoku_grid = [int(char)
                               for char in list(encoded_sudoku_grid)[::-1]]
        self.grid = [[Cell(0, 0, 0) for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for column in range(9):
                self.grid[row][column] = Cell(
                    row, column, value=encoded_sudoku_grid.pop())
        self.update_candidates_in_all_cells()

    def __eq__(self, other: GridInterface) -> bool:
        for row in range(9):
            for column in range(9):
                if self.get_cell(row, column).get_candidates() != other.get_cell(row, column).get_candidates():
                    return False

        return self.decode() == other.decode()

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

        excluded_values_from_same_row_column_grid = set(self.get_other_cells_on_column_by_cell(cell).get_marked_values() +
                                                        self.get_other_cells_on_row_by_cell(cell).get_marked_values() +
                                                        self.get_other_cells_in_grid_by_cell(cell).get_marked_values())
        cell.set_candidates(
            cell.get_candidates().difference(excluded_values_from_same_row_column_grid))

    def update_candidates_in_cell_row_column_grid(self, cell):
        cells_to_update = set(list(self.get_other_cells_on_column_by_cell(cell).cells) +
                                   list(self.get_other_cells_on_row_by_cell(cell).cells) +
                                   list(self.get_other_cells_in_grid_by_cell(cell).cells))
        candidate_to_remove = cell.get_value()
        for cell in cells_to_update:
            cell.remove_candidate(candidate_to_remove)

    def get_other_cells_on_row(self, row: int, col: int):
        return CellGroup([cell for cell in self.grid[row] if cell.get_position() != (row, col)])

    def get_rows(self):
        return [CellGroup(row) for row in self.grid]

    def get_columns(self):
        transposed_grid = list(zip(*self.grid))
        return [CellGroup(column) for column in transposed_grid]

    # def get_cells_on_row(self, row: int):
    #     return CellGroup(self.grid[row])

    def get_empty_cells_on_row(self, row: int):
        return CellGroup([cell for cell in self.grid[row] if cell.is_empty()])

    def get_other_cells_on_column(self, row: int, col: int):
        return CellGroup([vector[col] for vector in self.grid if vector[col].get_position() != (row, col)])

    # def get_cells_on_column(self, col: int):
    #     return CellGroup([row[col] for row in self.grid if row[col].get_col() == col])

    def get_empty_cells_on_col(self, col: int):
        return CellGroup([row[col] for row in self.grid if row[col].get_col() == col and row[col].is_empty()])

    def get_other_cells_in_grid(self, row: int, col: int):
        return CellGroup([cell for cell in self.get_square(
            row, col).flatten() if cell.get_position() != (row, col)])

    def get_other_cells_on_row_by_cell(self, main_cell: Cell):
        return CellGroup([cell for cell in self.grid[main_cell.get_row()] if cell.get_position() != main_cell.get_position()])

    def get_other_cells_on_column_by_cell(self, main_cell: Cell):
        return CellGroup([vector[main_cell.get_col()] for vector in self.grid if vector[main_cell.get_col()].get_position() != main_cell.get_position()])

    def get_other_cells_in_grid_by_cell(self, main_cell: Cell):
        return CellGroup([cell for cell in self.get_square(
            main_cell.get_row(), main_cell.get_col()).flatten() if cell.get_position() != main_cell.get_position()])

    def get_cell(self, row: int, col: int) -> CellInterface:
        return self.grid[row][col]

    def get_all_cells(self) -> list:
        return [self.get_cell(row, col) for row in range(0, 9) for col in range(0, 9)]

    # def get_all_unmarked_cells(self) -> list:
    #     return [cell for cell in self.get_all_cells() if cell.is_empty()]

    def get_square(self, row: int, col: int) -> SquareInterface:
        return Square(square=[rows[col//3*3: col//3*3+3] for rows in self.grid[row//3*3: row//3*3+3]])

    def get_all_squares(self) -> list:
        return [self.get_square(row, col) for row in range(0, 9, 3) for col in range(0, 9, 3)]

    def set_cell_value(self, cell: Cell, value: int):
        cell.set_value(value)
        self.update_candidates_in_cell_row_column_grid(cell)

    def show(self) -> None:
        grid_draw = '-'*25
        reversed_values = list(self.decode().replace('0', ' '))[:: -1]
        for _ in range(3):  # 3 rows of squares
            for _ in range(3):  # 3 rows
                grid_draw += '\n| '
                for _ in range(3):  # 3 horizontal squares
                    for _ in range(3):  # 3 inside square
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
