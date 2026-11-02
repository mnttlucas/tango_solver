import cv2

from vision.image_loader import load_image
from vision.grid_detector import GridDetector
from vision.cell_extractor import CellExtractor

image = load_image("assets/screenshot-01.png")

board_image = GridDetector().crop(image)

cells = CellExtractor().extract(board_image)

sun_cell = cells[0][0]

print(cv2.imwrite("assets/templates/empty.png", sun_cell))
