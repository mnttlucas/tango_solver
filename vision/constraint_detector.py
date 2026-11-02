import cv2
import numpy as np

from tango.constraints import Constraint, ConstraintType


class ConstraintDetector:
    """Finds the '=' and 'x' signs sitting on the line between two cells."""

    # Half-size of the inspected patch, as a share of the cell size.
    # Small enough to stay clear of the sun/moon glyphs of both cells.
    PATCH = 0.18

    # Pixels darker than this (gray level) belong to a sign. The grid lines
    # are much paler (around 230) and the signs are brown (around 115).
    DARK_LEVEL = 190

    # Share of the patch that must be dark for a sign to be present.
    MIN_RATIO = 0.015

    def detect(self, board_image, size=6):
        """Returns the list of Constraint found on the board."""
        gray = cv2.cvtColor(board_image, cv2.COLOR_BGR2GRAY)

        height, width = gray.shape
        cell_h = height / size
        cell_w = width / size

        constraints = []

        for row in range(size):
            for col in range(size):
                if col + 1 < size:
                    center = ((col + 1) * cell_w, (row + 0.5) * cell_h)
                    kind = self.classify(gray, center, cell_w, cell_h)

                    if kind is not None:
                        constraints.append(Constraint((row, col), (row, col + 1), kind))

                if row + 1 < size:
                    center = ((col + 0.5) * cell_w, (row + 1) * cell_h)
                    kind = self.classify(gray, center, cell_w, cell_h)

                    if kind is not None:
                        constraints.append(Constraint((row, col), (row + 1, col), kind))

        return constraints

    def classify(self, gray, center, cell_w, cell_h):
        """ConstraintType of the sign at `center` (image pixels), or None."""
        half_x = int(cell_w * self.PATCH)
        half_y = int(cell_h * self.PATCH)

        cx, cy = int(round(center[0])), int(round(center[1]))

        x1, x2 = max(0, cx - half_x), min(gray.shape[1], cx + half_x)
        y1, y2 = max(0, cy - half_y), min(gray.shape[0], cy + half_y)

        patch = gray[y1:y2, x1:x2]

        if patch.size == 0:
            return None

        dark = patch < self.DARK_LEVEL

        if dark.sum() / dark.size < self.MIN_RATIO:
            return None

        ys, xs = np.nonzero(dark)

        width = xs.max() - xs.min() + 1
        height = ys.max() - ys.min() + 1

        glyph = dark[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        glyph = cv2.resize(
            glyph.astype(np.float32), (15, 15), interpolation=cv2.INTER_AREA
        )

        # Two cues, because blur at small sizes weakens either of them alone:
        # - 'x' crosses at its center, '=' leaves a gap between its two bars;
        # - 'x' is about as wide as tall, '=' is clearly wider than tall.
        center_mass = glyph[6:9, 6:9].mean()
        aspect = width / height

        if center_mass - 2.5 * (aspect - 1.1) > 0.45:
            return ConstraintType.DIFFERENT

        return ConstraintType.EQUAL
