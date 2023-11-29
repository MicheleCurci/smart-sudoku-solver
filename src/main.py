from cyclic_pipeline import CyclicPipeline
from sudoku_grid import SudokuGrid
from sudoku_techniques import SingleCandidateTechnique, IsolateCandidatesInSquareTechnique, IsolateCandidatesInRowsAndColumnsTechnique, DoubleCoupleTechnique, DoubleCoupleAlignedTechnique, ThreeCandidatesInThreeCellsTechnique
import time


def is_grid_filled(grid: SudokuGrid):
    return grid.is_filled()


def main():

    sudoku_cyclic_pipeline = CyclicPipeline(
        [SingleCandidateTechnique(), IsolateCandidatesInSquareTechnique(), IsolateCandidatesInRowsAndColumnsTechnique(), DoubleCoupleTechnique(), DoubleCoupleAlignedTechnique(), ThreeCandidatesInThreeCellsTechnique()])

    grid = SudokuGrid(
        # 100 iterations
        # "060372000050000030020500970200015004003090600400630002097001060030000040000763020"
        "080020560000100007000000000050090408007800003090010050204000800060085000000200100"
    )
    # grid.show()

    st = time.time()
    sudoku_cyclic_pipeline.start(grid, stop_condition=is_grid_filled)
    et = time.time()

    grid.show()
    solution = grid.decode()
    # real_solution = "968372415754189236321546978276815394513294687489637152897421563632958741145763829"
    real_solution = "483729561529146387716538249152693478647852913398417652274961835961385724835274196"
    if (real_solution == solution):
        print("!!!!! SUCCESS !!!!!")

    exec_time = (et - st) * 1000
    print('Execution time:', exec_time, 'ms')

    # for cell in grid.get_all_unmarked_cells():
    #     print("-- cell " + str(cell.get_position()) +
    #           " " + str(cell.get_candidates()))


if __name__ == "__main__":
    main()
