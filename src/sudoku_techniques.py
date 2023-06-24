from job_interface import JobInterface
from sudoku_grid_interface import SudokuGridInterface, SubGridInterface, VectorInterface
from sudoku_grid import Vector


# class Result():
#     def __init__(self, grid: SudokuGridInterface, has_marked_in_last_run: bool) -> None:
#         self.grid = grid
#         self.has_marked_in_last_run = has_marked_in_last_run

# single candidate:
# - in cell
# - in row
# - in column
# - in grid
class SingleCandidateTechnique(JobInterface):
    def __init__(self) -> None:
        pass

    def run(self, grid: SudokuGridInterface) -> SudokuGridInterface:
        # mark cells with unique candidates
        # TODO: replace with get_all_cells()
        for row in range(0, 9):
            for col in range(0, 9):
                cell = grid.get_cell(row, col)
                if cell.is_marked():
                    continue

                candidates = cell.get_candidates()

                # Tecnique (basic): single candidate

                if len(candidates) == 1:
                    grid.set_cell_value(cell, list(candidates)[0])
                    return grid

                # Tecnique: Stucked candidate type 1 (+ check in subgrid)
                cells_on_same_row = grid.get_other_cells_on_row(row, col)
                cells_on_same_column = grid.get_other_cells_on_column(row, col)
                cells_in_same_grid = grid.get_other_cells_in_grid(row, col)

                candidates_in_same_row_column_and_grid = [cells_on_same_row.get_candidates_union(
                ), cells_on_same_column.get_candidates_union(), cells_in_same_grid.get_candidates_union()]

                for candidates_group in candidates_in_same_row_column_and_grid:
                    unique_candidates_in_group = candidates.difference(
                        candidates_group)
                    if len(unique_candidates_in_group) == 1:
                        grid.set_cell_value(cell, list(
                            unique_candidates_in_group)[0])
                        return grid  # Result(grid, True)

        return grid  # Result(grid, False)

# Tecnique: Stucked candidate type 1


class IsolateCandidatesInSubgridTechnique(JobInterface):

    def __init__(self) -> None:
        pass

    def run(self, grid: SudokuGridInterface) -> SudokuGridInterface:

        for subgrid in grid.get_all_sub_grids():

            for row in subgrid.get_rows():
                empty_cells_in_subrow = Vector(
                    [cell for cell in row.cells if cell.is_empty()])

                if len(empty_cells_in_subrow.cells) == 0:
                    continue

                row_index = empty_cells_in_subrow.cells[0].get_row()

                empty_cells_on_same_row_in_other_subgrids = grid.get_empty_cells_on_row(
                    row_index).difference(empty_cells_in_subrow)

                unique_candidates_in_subrow = empty_cells_in_subrow.get_candidates_union(
                ).difference(Vector(empty_cells_on_same_row_in_other_subgrids).get_candidates_union())

                if len(unique_candidates_in_subrow) == 0:
                    continue

                other_empty_cells_in_subgrid = subgrid.get_other_empty_cells_in_subgrid(
                    empty_cells_in_subrow.cells)

                for cell in other_empty_cells_in_subgrid.cells:
                    cell.remove_candidates(unique_candidates_in_subrow)

            # same logic on columns
            for column in subgrid.get_columns():

                empty_cells_in_subcolumn = Vector(
                    [cell for cell in column.cells if cell.is_empty()])

                if len(empty_cells_in_subcolumn.cells) == 0:
                    continue

                col_index = empty_cells_in_subcolumn.cells[0].get_col()

                empty_cells_on_same_column_in_other_subgrids = grid.get_empty_cells_on_col(
                    col_index).difference(empty_cells_in_subcolumn)

                unique_candidates_in_subcol = empty_cells_in_subcolumn.get_candidates_union(
                ).difference(Vector(empty_cells_on_same_column_in_other_subgrids).get_candidates_union())

                if len(unique_candidates_in_subcol) == 0:
                    continue

                other_empty_cells_in_subgrid = subgrid.get_other_empty_cells_in_subgrid(
                    empty_cells_in_subcolumn.cells)

                for cell in other_empty_cells_in_subgrid.cells:
                    cell.remove_candidates(unique_candidates_in_subcol)

        return grid


class IsolateCandidatesInRowsAndColumnsTechnique(JobInterface):

    def __init__(self) -> None:
        pass

    def run(self, grid: SudokuGridInterface) -> SudokuGridInterface:

        for subgrid in grid.get_all_sub_grids():

            for row in subgrid.get_rows():
                empty_cells_in_subrow = Vector(
                    [cell for cell in row.cells if cell.is_empty()])

                if len(empty_cells_in_subrow.cells) == 0:
                    continue

                row_index = empty_cells_in_subrow.cells[0].get_row()

                other_empty_cells_in_subgrid = subgrid.get_other_empty_cells_in_subgrid(
                    empty_cells_in_subrow.cells)

                empty_cells_on_same_row_in_other_subgrids = Vector(grid.get_empty_cells_on_row(
                    row_index).difference(empty_cells_in_subrow))

                unique_candidates_in_subrow = empty_cells_in_subrow.get_candidates_union(
                ).difference(other_empty_cells_in_subgrid.get_candidates_union())

                if len(unique_candidates_in_subrow) == 0:
                    continue

                for cell in empty_cells_on_same_row_in_other_subgrids.cells:
                    cell.remove_candidates(unique_candidates_in_subrow)

            # same logic on columns
            for column in subgrid.get_columns():
                empty_cells_in_subcol = Vector(
                    [cell for cell in column.cells if cell.is_empty()])

                if len(empty_cells_in_subcol.cells) == 0:
                    continue

                col_index = empty_cells_in_subcol.cells[0].get_col()

                other_empty_cells_in_subgrid = subgrid.get_other_empty_cells_in_subgrid(
                    empty_cells_in_subcol.cells)

                empty_cells_on_same_col_in_other_subgrids = Vector(grid.get_empty_cells_on_col(
                    col_index).difference(empty_cells_in_subcol))

                unique_candidates_in_subcol = empty_cells_in_subcol.get_candidates_union(
                ).difference(other_empty_cells_in_subgrid.get_candidates_union())

                if len(unique_candidates_in_subcol) == 0:
                    continue

                for cell in empty_cells_on_same_col_in_other_subgrids.cells:
                    cell.remove_candidates(unique_candidates_in_subcol)

        return grid


class DoubleCoupleTechnique(JobInterface):

    def __init__(self) -> None:
        pass

    def run(self, grid: SudokuGridInterface) -> SudokuGridInterface:

        for subgrid in grid.get_all_sub_grids():

            cells_with_2_candidates = [
                cell for cell in subgrid.get_empty_cells() if len(cell.get_candidates()) == 2]

            for cell_1 in cells_with_2_candidates:
                for cell_2 in cells_with_2_candidates:
                    if cell_1 == cell_2 or cell_1.get_candidates() != cell_2.get_candidates():
                        continue

                    common_candidates = cell_1.get_candidates()
                    for sibling_cell in subgrid.get_other_empty_cells_in_subgrid([cell_1, cell_2]).cells:
                        sibling_cell.remove_candidates(common_candidates)
        return grid


# USELESS???
class DoubleCoupleAlignedTechnique(JobInterface):

    def __init__(self) -> None:
        pass

    def run(self, grid: SudokuGridInterface) -> SudokuGridInterface:

        for row in grid.get_rows():

            cells_with_2_candidates = [
                cell for cell in row.get_unmarked_cells() if len(cell.get_candidates()) == 2]

            for cell_1 in cells_with_2_candidates:
                for cell_2 in cells_with_2_candidates:
                    if cell_1 == cell_2 or cell_1.get_candidates() != cell_2.get_candidates():
                        continue

                    common_candidates = cell_1.get_candidates()
                    for cell_on_same_row in row.difference(Vector([cell_1, cell_2])):
                        cell_on_same_row.remove_candidates(common_candidates)

        for col in grid.get_columns():

            cells_with_2_candidates = [
                cell for cell in col.get_unmarked_cells() if len(cell.get_candidates()) == 2]

            for cell_1 in cells_with_2_candidates:
                for cell_2 in cells_with_2_candidates:
                    if cell_1 == cell_2 or cell_1.get_candidates() != cell_2.get_candidates():
                        continue

                    common_candidates = cell_1.get_candidates()
                    for cell_on_same_col in col.difference(Vector([cell_1, cell_2])):
                        cell_on_same_col.remove_candidates(common_candidates)
        return grid

# !!! ONLY ON ROWS
# TODO: extend algorithm for column and inner grid too


class ThreeCandidatesInThreeCellsTechnique(JobInterface):

    def __init__(self) -> None:
        pass

    def run(self, grid: SudokuGridInterface) -> SudokuGridInterface:

        for row in grid.get_rows():

            empty_cells_in_row = [
                cell for cell in row.get_unmarked_cells()]

            for cell_1 in empty_cells_in_row:
                for cell_2 in empty_cells_in_row:
                    for cell_3 in empty_cells_in_row:
                        if len({cell_1, cell_2, cell_3}) != 3:  # check distinct cells
                            continue
                        triple_candidates_union = Vector(
                            [cell_1, cell_2, cell_3]).get_candidates_union()

                        other_cells_on_row_candidates = Vector(list(set(empty_cells_in_row).difference(
                            {cell_1, cell_2, cell_3}))).get_candidates_union()

                        if len(triple_candidates_union.difference(other_cells_on_row_candidates)) == 3:
                            for cell in [cell_1, cell_2, cell_3]:
                                cell.remove_candidates(
                                    other_cells_on_row_candidates)
                            # return grid ...to speed up because it's rare

        # COLUMN...
        # GRID...

        return grid