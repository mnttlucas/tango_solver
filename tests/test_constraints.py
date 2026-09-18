import unittest

from tango.board import Board
from tango.constraints import Constraint, ConstraintType
from tango.enums import Symbol

class TestConstraints(unittest.TestCase):
	def test_equal_constraint_valid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(0, 1, Symbol.SUN)
		board.add_constraint(Constraint((0, 0),	(0, 1),	ConstraintType.EQUAL))
		self.assertTrue(board.is_valid())

	def test_equal_constraint_invalid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(0, 1, Symbol.MOON)
		board.add_constraint(Constraint((0, 0), (0, 1), ConstraintType.EQUAL))
		self.assertFalse(board.is_valid())

	def test_different_constraint_valid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(0, 1, Symbol.MOON)
		board.add_constraint(Constraint((0, 0),	(0, 1),	ConstraintType.DIFFERENT))
		self.assertTrue(board.is_valid())

	def test_different_constraint_invalid(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(0, 1, Symbol.SUN)
		board.add_constraint(Constraint((0, 0),	(0, 1),	ConstraintType.DIFFERENT))
		self.assertFalse(board.is_valid())

	def test_constraint_with_empty_cells(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.add_constraint(Constraint((0, 0),	(0, 1),	ConstraintType.EQUAL))
		self.assertTrue(board.is_valid())

	def test_multiple_constraints(self):
		board = Board()
		board.set_cell(0, 0, Symbol.SUN)
		board.set_cell(0, 1, Symbol.SUN)
		board.set_cell(0, 2, Symbol.MOON)
		board.add_constraint(Constraint((0, 0), (0, 1),	ConstraintType.EQUAL))
		board.add_constraint(Constraint((0, 1),	(0, 2),	ConstraintType.DIFFERENT))
		self.assertTrue(board.is_valid())