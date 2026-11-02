from tango.board import Board
from tango.constraints import Constraint, ConstraintType
from tango.enums import Symbol
from tango.solver import Solver
from vision.image_loader import load_image
from vision.grid_detector import GridDetector
from vision.cell_extractor import CellExtractor

import cv2

image = load_image("assets/screenshot-01.png")

print("Shape:", image.shape)

cv2.imshow("Screenshot", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


""" # Real LinkedIn puzzle (18/09/2026)
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
print(board) """

image = load_image("assets/screenshot-01.png")

detector = GridDetector()

board_image = detector.crop(image)

extractor = CellExtractor()

cells = extractor.extract(
    board_image
)

print(
    f"{len(cells)} rows"
)

print(
    f"{len(cells[0])} columns"
)

cv2.imshow(
    "Board",
    board_image
)

cv2.waitKey(0)
cv2.destroyAllWindows()