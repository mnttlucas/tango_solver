import unittest

from tango.board import Board
from tango.enums import Symbol

class TestRows(unittest.TestCase):
	def test_row_with_three_non_consecutive_suns_is_valid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(0, 2, Symbol.SUN)
		board.set_cell(0, 4, Symbol.SUN)
		self.assertTrue(board.is_valid())

	def test_row_with_four_suns_is_invalid(self):
		board = Board()
		for col in range(4):
			board.set_cell(0, col, Symbol.SUN)
		self.assertFalse(board.is_valid())

	def test_row_with_four_moons_is_invalid(self):
		board = Board()
		for col in range(4):
			board.set_cell(0, col, Symbol.MOON)
		self.assertFalse(board.is_valid())