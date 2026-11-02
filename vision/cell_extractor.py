class CellExtractor:

    def extract(self, board_image, size=6):
        """Cuts the board image into size x size cells, as cells[row][col]."""
        height, width = board_image.shape[:2]

        # Round each border from the exact position, so the error never builds up.
        xs = [round(col * width / size) for col in range(size + 1)]
        ys = [round(row * height / size) for row in range(size + 1)]

        return [
            [board_image[ys[row]:ys[row + 1], xs[col]:xs[col + 1]] for col in range(size)]
            for row in range(size)
        ]
