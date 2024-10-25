import pytest
from src.pipeline.cyclic_pipeline import CyclicPipeline
from src.sudoku.grid import Grid
from src.sudoku.techniques import (
    SingleCandidateTechnique,
    IsolateCandidatesInSquareTechnique,
    IsolateCandidatesInRowsAndColumnsTechnique,
    DoubleCoupleTechnique,
    DoubleCoupleAlignedTechnique,
    ThreeCandidatesInThreeCellsTechnique,
)


@pytest.fixture
def sudoku_cyclic_pipeline():
    return CyclicPipeline(
        [
            SingleCandidateTechnique(),
            IsolateCandidatesInSquareTechnique(),
            IsolateCandidatesInRowsAndColumnsTechnique(),
            DoubleCoupleTechnique(),
            DoubleCoupleAlignedTechnique(),
            ThreeCandidatesInThreeCellsTechnique(),
        ]
    )


def is_grid_filled(grid: Grid):
    return grid.is_filled()


def test_easy_sudoku_success(sudoku_cyclic_pipeline):
    encoded_sudoku_grid = [
        [0, 6, 0, 3, 7, 2, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 3, 0],
        [0, 2, 0, 5, 0, 0, 9, 7, 0],
        [2, 0, 0, 0, 1, 5, 0, 0, 4],
        [0, 0, 3, 0, 9, 0, 6, 0, 0],
        [4, 0, 0, 6, 3, 0, 0, 0, 2],
        [0, 9, 7, 0, 0, 1, 0, 6, 0],
        [0, 3, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 7, 6, 3, 0, 2, 0],
    ]

    grid = Grid(encoded_sudoku_grid)
    sudoku_cyclic_pipeline.start(grid, stop_condition=is_grid_filled)
    actual = grid

    expected = Grid(
        [
            [9, 6, 8, 3, 7, 2, 4, 1, 5],
            [7, 5, 4, 1, 8, 9, 2, 3, 6],
            [3, 2, 1, 5, 4, 6, 9, 7, 8],
            [2, 7, 6, 8, 1, 5, 3, 9, 4],
            [5, 1, 3, 2, 9, 4, 6, 8, 7],
            [4, 8, 9, 6, 3, 7, 1, 5, 2],
            [8, 9, 7, 4, 2, 1, 5, 6, 3],
            [6, 3, 2, 9, 5, 8, 7, 4, 1],
            [1, 4, 5, 7, 6, 3, 8, 2, 9],
        ]
    )

    assert actual.is_valid()
    assert actual == expected


def test_hard_sudoku_success(sudoku_cyclic_pipeline):
    encoded_sudoku_grid = "080020560000100007000000000050090408007800003090010050204000800060085000000200100"
    grid = Grid(encoded_sudoku_grid)
    sudoku_cyclic_pipeline.start(grid, stop_condition=is_grid_filled)
    actual = grid.encode()
    expected = "483729561529146387716538249152693478647852913398417652274961835961385724835274196"
    assert actual == expected
    assert grid.is_valid()


def test_sudoku_failure(sudoku_cyclic_pipeline):
    encoded_sudoku_grid = "080020560000100007000000000050090408007800003090010050204000800060085000000200100"
    grid = Grid(encoded_sudoku_grid)
    sudoku_cyclic_pipeline.start(grid, stop_condition=is_grid_filled)
    actual = grid.encode()
    expected = "783729567529146387716538249152693478647852913398417652274961835961385724835274196"
    assert actual != expected
