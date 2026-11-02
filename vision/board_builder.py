from tango.board import Board

from vision.symbol_detector import SymbolDetector


class BoardBuilder:

    def __init__(self):
        self.symbol_detector = SymbolDetector()

    def build(self, cells):
        board = Board()

        for row in range(board.size):
            for col in range(board.size):
                board.set_cell(row, col, self.symbol_detector.detect(cells[row][col]))

        return board
