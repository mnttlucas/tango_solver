from tango.board import Board
from tango.constraints import Constraint, ConstraintType
from tango.enums import Symbol
from tango.solver import Solver

# Real LinkedIn puzzle (18/09/2026)
board = Board()
board.set_cell(0, 0, Symbol.SUN)
board.set_cell(1, 0, Symbol.SUN)
board.set_cell(1, 2, Symbol.SUN)
board.set_cell(2, 0, Symbol.MOON)
board.set_cell(2, 1, Symbol.SUN)
board.set_cell(2, 2, Symbol.SUN)
board.add_constraint(Constraint((3, 3), (4, 3), ConstraintType.DIFFERENT))
board.add_constraint(Constraint((4, 3), (5, 3), ConstraintType.DIFFERENT))
board.add_constraint(Constraint((4, 5), (5, 5), ConstraintType.EQUAL))
board.add_constraint(Constraint((5, 3), (5, 4), ConstraintType.DIFFERENT))
board.add_constraint(Constraint((5, 4), (5, 5), ConstraintType.EQUAL))

print("Valid board ?", board.is_valid(), "\nInitial board state :\n")
print(board)

solver = Solver()
solver.solve(board)

print("\nSolved board :\n")
print(board)