class BoardGeometry:
    """Where the board sits in the image it was detected in."""

    def __init__(self, x, y, size, grid_size=6):
        self.x = x
        self.y = y
        self.size = size
        self.grid_size = grid_size

    @property
    def cell_size(self):
        return self.size / self.grid_size

    def cell_center(self, row, col):
        """Pixel (x, y) of the center of a cell, in the source image."""
        return (
            self.x + (col + 0.5) * self.cell_size,
            self.y + (row + 0.5) * self.cell_size,
        )

    def __repr__(self):
        return f"BoardGeometry(x={self.x}, y={self.y}, size={self.size})"
