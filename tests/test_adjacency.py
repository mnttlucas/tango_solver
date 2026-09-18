import unittest

from tango.board import Board
from tango.enums import Symbol

class TestAdjacency(unittest.TestCase):
	def test_three_moons_horizontal_is_invalid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.MOON)
		board.set_cell(0, 1, Symbol.MOON)
		board.set_cell(0, 2, Symbol.MOON)
		self.assertFalse(board.is_valid())

	def test_three_suns_horizontal_is_invalid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(0, 1, Symbol.SUN)
		board.set_cell(0, 2, Symbol.SUN)
		self.assertFalse(board.is_valid())

	def test_three_suns_vertical_is_invalid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(1, 0, Symbol.SUN)
		board.set_cell(2, 0, Symbol.SUN)
		self.assertFalse(board.is_valid())

	def test_two_suns_is_valid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(0, 1, Symbol.SUN)
		self.assertTrue(board.is_valid())

	def test_sun_moon_sun_is_valid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(0, 1, Symbol.MOON)
		board.set_cell(0, 2, Symbol.SUN)
		self.assertTrue(board.is_valid())