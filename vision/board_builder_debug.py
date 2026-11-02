from vision.image_loader import load_image
from vision.grid_detector import GridDetector
from vision.cell_extractor import CellExtractor
from vision.board_builder import BoardBuilder

image = load_image("assets/screenshot-01.png")

board_image = GridDetector().crop(image)

cells = CellExtractor().extract(board_image)

board = BoardBuilder().build(cells)

print(board)