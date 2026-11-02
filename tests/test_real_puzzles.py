import copy
import unittest
from pathlib import Path

import cv2

from tango.board import Board
from tango.solver import Solver
from vision.board_reader import BoardReader

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def read(name):
    return BoardReader().read(cv2.imread(str(ASSETS / name))).board


class TestRealPuzzles(unittest.TestCase):
    def test_each_puzzle_has_exactly_one_solution(self):
        for name in ("screenshot-01.png", "screenshot-02.jpg"):
            with self.subTest(name):
                self.assertEqual(Solver().count_solutions(read(name)), 1)

    def test_solver_finds_a_valid_solution(self):
        for name in ("screenshot-01.png", "screenshot-02.jpg"):
            with self.subTest(name):
                board = read(name)
                self.assertTrue(Solver().solve(board))
                self.assertTrue(board.is_solved())

    def test_solver_reproduces_the_solved_screenshot(self):
        solved = read("solved-example.jpg")

        # Only the cells that were given at the start, plus the constraints.
        puzzle = Board()
        for row, col in [(0, 0), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]:
            puzzle.set_cell(row, col, solved.get_cell(row, col))
        for constraint in solved.constraints:
            puzzle.add_constraint(constraint)

        self.assertEqual(Solver().count_solutions(puzzle), 1)

        Solver().solve(puzzle)
        self.assertEqual(puzzle.grid, solved.grid)

    def test_count_solutions_leaves_the_board_untouched(self):
        board = read("screenshot-02.jpg")
        before = copy.deepcopy(board.grid)

        Solver().count_solutions(board)

        self.assertEqual(board.grid, before)


if __name__ == "__main__":
    unittest.main()
