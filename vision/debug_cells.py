import cv2

from vision.image_loader import load_image
from vision.grid_detector import GridDetector
from vision.cell_extractor import CellExtractor

image = load_image("assets/screenshot-01.png")

board_image = (GridDetector().crop(image))

cells = (CellExtractor().extract(board_image))

cell = cells[0][0]

print(cell.shape)
height, width = cell.shape[:2]

print(height)
print(width)

cv2.imshow("Cell", cell)
cv2.waitKey(0)
cv2.destroyAllWindows()