import unittest

from tango.board import Board
from tango.enums import Symbol

class TestSolved(unittest.TestCase):
	def test_complete_valid_board(self):
		board = Board()

		values = [
			[1, 1, 2, 2, 1, 2],
			[2, 2, 1, 1, 2, 1],
			[1, 2, 1, 2, 1, 2],
			[2, 1, 2, 1, 2, 1],
			[1, 2, 2, 1, 2, 1],
			[2, 1, 1, 2, 1, 2],
		]

		for row in range(6):
			for col in range(6):
				board.set_cell(row, col, Symbol.SUN if values[row][col] == 1 else Symbol.MOON)
		self.assertTrue(board.is_solved())

	def test_incomplete_board_not_solved(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		self.assertFalse(board.is_solved())

	def test_complete_board_wrong_balance(self):
		board = Board()

		values = [
			[1, 1, 1, 1, 2, 2],
			[2, 2, 1, 1, 2, 1],
			[1, 2, 1, 2, 1, 2],
			[2, 1, 2, 1, 2, 1],
			[1, 2, 2, 1, 2, 1],
			[2, 1, 1, 2, 1, 2],
		]

		for row in range(6):
			for col in range(6):
				board.set_cell(row, col, Symbol.SUN if values[row][col] == 1 else Symbol.MOON)
		self.assertFalse(board.is_solved())