from cyclic_pipeline import CyclicPipeline
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
        "080020560000100007000000000050090408007800003090010050204000800060085000000200100"
    )
    grid.show()

    st = time.time()
    sudoku_cyclic_pipeline.start(grid, stop_condition=is_grid_filled)
    et = time.time()

    grid.show()
    solution = grid.decode()
    real_solution = "483729561529146387716538249152693478647852913398417652274961835961385724835274196"
    if real_solution == solution:
        print("> SUDOKU SOLVED!")

    exec_time = (et - st) * 1000
    print("Execution time:", exec_time, "ms")


if __name__ == "__main__":
    main()
