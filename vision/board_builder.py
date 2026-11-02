from tango.board import Board
from tango.enums import Symbol

from vision.symbol_detector import (
    SymbolDetector,
    CellContent
)


class BoardBuilder:

    def __init__(self):
        self.symbol_detector = SymbolDetector()

    def build(self, cells):
        board = Board()

        for row in range(6):
            for col in range(6):
                content = self.symbol_detector.detect(
                    cells[row][col]
                )

                if content == CellContent.SUN:
                    board.set_cell(
                        row,
                        col,
                        Symbol.SUN
                    )

                elif content == CellContent.MOON:
                    board.set_cell(
                        row,
                        col,
                        Symbol.MOON
                    )

        return board