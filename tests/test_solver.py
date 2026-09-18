import unittest

from tango.board import Board
from tango.enums import Symbol
from tango.solver import Solver

class TestSolver(unittest.TestCase):
	def test_solve_almost_complete_board(self):
		board = Board()

		values = [
			[1, 1, 2, 2, 1, 2],
			[2, 2, 1, 1, 2, 1],
			[1, 2, 1, 2, 1, 2],
			[2, 1, 2, 1, 2, 1],
			[1, 2, 2, 1, 2, 1],
			[2, 1, 1, 2, 1, 0],
		]

		for row in range(board.size):
			for col in range(board.size):
				value = values[row][col]

				if value == 0:
					continue

				board.set_cell(row, col, Symbol.SUN if value == 1 else Symbol.MOON)

		solver = Solver()

		self.assertTrue(solver.solve(board))
		self.assertTrue(board.is_solved())