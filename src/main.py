from src.cyclic_pipeline import CyclicPipeline
from src.sudoku_entities import Grid
from src.sudoku_techniques import (
    SingleCandidateTechnique,
    IsolateCandidatesInSquareTechnique,
    IsolateCandidatesInRowsAndColumnsTechnique,
    DoubleCoupleTechnique,
    DoubleCoupleAlignedTechnique,
    ThreeCandidatesInThreeCellsTechnique,
)
import time


def is_grid_filled(grid: Grid):
    return grid.is_filled()


def main():
    sudoku_cyclic_pipeline = CyclicPipeline(
        [
            SingleCandidateTechnique(),
            IsolateCandidatesInSquareTechnique(),
            IsolateCandidatesInRowsAndColumnsTechnique(),
            DoubleCoupleTechnique(),
            DoubleCoupleAlignedTechnique(),
            ThreeCandidatesInThreeCellsTechnique(),
        ]
    )

    grid = Grid(
        [
            [0, 8, 0, 0, 2, 0, 5, 6, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 9, 0, 4, 0, 8],
            [0, 0, 7, 8, 0, 0, 0, 0, 3],
            [0, 9, 0, 0, 1, 0, 0, 5, 0],
            [2, 0, 4, 0, 0, 0, 8, 0, 0],
            [0, 6, 0, 0, 8, 5, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 1, 0, 0],
        ]
    )
    grid.show()

    st = time.time()
    sudoku_cyclic_pipeline.start(grid, stop_condition=is_grid_filled)
    et = time.time()

    grid.show()
    solution = grid.encode()
    real_solution = [
        [4, 8, 3, 7, 2, 9, 5, 6, 1],
        [5, 2, 9, 1, 4, 6, 3, 8, 7],
        [7, 1, 6, 5, 3, 8, 2, 4, 9],
        [1, 5, 2, 6, 9, 3, 4, 7, 8],
        [6, 4, 7, 8, 5, 2, 9, 1, 3],
        [3, 9, 8, 4, 1, 7, 6, 5, 2],
        [2, 7, 4, 9, 6, 1, 8, 3, 5],
        [9, 6, 1, 3, 8, 5, 7, 2, 4],
        [8, 3, 5, 2, 7, 4, 1, 9, 6],
    ]
    if real_solution == solution:
        print("> SUDOKU SOLVED!")

    exec_time = (et - st) * 1000
    print("Execution time:", exec_time, "ms")


if __name__ == "__main__":
    main()
