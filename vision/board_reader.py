from vision.board_builder import BoardBuilder
from vision.cell_extractor import CellExtractor
from vision.constraint_detector import ConstraintDetector
from vision.geometry import BoardGeometry
from vision.grid_detector import GridDetector


class BoardNotFound(ValueError):
    pass


class BoardMisread(ValueError):
    pass


class BoardReading:
    """Result of reading a screenshot: the puzzle and where it is on screen."""

    def __init__(self, board, geometry):
        self.board = board
        self.geometry = geometry


class BoardReader:
    """Screenshot in, Board (givens + constraints) and its position out."""

    def __init__(self):
        self.grid_detector = GridDetector()
        self.cell_extractor = CellExtractor()
        self.board_builder = BoardBuilder()
        self.constraint_detector = ConstraintDetector()

    def read(self, image):
        rect = self.grid_detector.detect(image)

        if rect is None:
            raise BoardNotFound("No Tango board found in the image")

        x, y, w, h = rect
        board_image = image[y:y + h, x:x + w]

        cells = self.cell_extractor.extract(board_image)

        try:
            board = self.board_builder.build(cells)
        except ValueError as error:
            raise BoardMisread(str(error)) from error

        for constraint in self.constraint_detector.detect(board_image):
            board.add_constraint(constraint)

        if not board.is_valid():
            raise BoardMisread(
                "The board read from the image breaks the rules, "
                "so it was probably misread:\n" + str(board)
            )

        return BoardReading(board, BoardGeometry(x, y, w))

