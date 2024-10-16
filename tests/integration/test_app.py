import unittest
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


class TestSudoku(unittest.TestCase):
    def setUp(self):
        self.sudoku_cyclic_pipeline = CyclicPipeline(
            [
                SingleCandidateTechnique(),
                IsolateCandidatesInSquareTechnique(),
                IsolateCandidatesInRowsAndColumnsTechnique(),
                DoubleCoupleTechnique(),
                DoubleCoupleAlignedTechnique(),
                ThreeCandidatesInThreeCellsTechnique(),
            ]
        )

    def is_grid_filled(self, grid: Grid):
        return grid.is_filled()

    def test_easy_sudoku_success(self):
        encoded_sudoku_grid = "060372000050000030020500970200015004003090600400630002097001060030000040000763020"
        grid = Grid(encoded_sudoku_grid)
        self.sudoku_cyclic_pipeline.start(grid, stop_condition=self.is_grid_filled)

        actual = grid.encode()
        expected = "968372415754189236321546978276815394513294687489637152897421563632958741145763829"

        self.assertEqual(actual, expected)
        self.assertEqual(grid.is_valid(), True)

    def test_hard_sudoku_success(self):
        encoded_sudoku_grid = "080020560000100007000000000050090408007800003090010050204000800060085000000200100"
        grid = Grid(encoded_sudoku_grid)
        self.sudoku_cyclic_pipeline.start(grid, stop_condition=self.is_grid_filled)

        actual = grid.encode()
        expected = "483729561529146387716538249152693478647852913398417652274961835961385724835274196"

        self.assertEqual(actual, expected)
        self.assertEqual(grid.is_valid(), True)

    def test_sudoku_failure(self):
        encoded_sudoku_grid = "080020560000100007000000000050090408007800003090010050204000800060085000000200100"
        grid = Grid(encoded_sudoku_grid)
        self.sudoku_cyclic_pipeline.start(grid, stop_condition=self.is_grid_filled)

        actual = grid.encode()
        expected = "783729567529146387716538249152693478647852913398417652274961835961385724835274196"

        self.assertNotEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
