from vision.image_loader import load_image
from vision.grid_detector import GridDetector
from vision.cell_extractor import CellExtractor
from vision.symbol_detector import SymbolDetector


image = load_image("assets/screenshot-01.png")

board_image = GridDetector().crop(image)

cells = CellExtractor().extract(board_image)

detector = SymbolDetector()

for row in range(6):
    for col in range(6):
        result = detector.detect(cells[row][col])

        print(f"({row},{col}) -> {result}")