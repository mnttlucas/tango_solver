import unittest

from tango.board import Board
from tango.enums import Symbol

class TestColumns(unittest.TestCase):

	def test_column_with_three_non_consecutive_suns_is_valid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(2, 0, Symbol.SUN)
		board.set_cell(4, 0, Symbol.SUN)
		self.assertTrue(board.is_valid())

	def test_column_with_four_suns_is_invalid(self):
		board = Board()

		for row in range(4):
			board.set_cell(row, 0, Symbol.SUN)

		self.assertFalse(board.is_valid())

	def test_column_with_four_moons_is_invalid(self):
		board = Board()

		for row in range(4):
			board.set_cell(row, 0, Symbol.MOON)

		self.assertFalse(board.is_valid())