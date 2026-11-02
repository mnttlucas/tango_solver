import cv2

from tango.enums import Symbol


class SymbolDetector:
    """Classifies a cell by the color of its glyph (orange sun / blue moon).

    Color based on purpose: unlike template matching it does not depend on the
    cell size in pixels, nor on the background of the cell (locked cells are
    beige, free cells are white).
    """

    # OpenCV hue range is 0..179
    SUN_HUE = (8, 32)
    MOON_HUE = (95, 130)

    MIN_SATURATION = 90
    MIN_VALUE = 80

    # Share of the (central part of the) cell that must be colored.
    MIN_RATIO = 0.03

    # Ignore the cell borders, where grid lines and neighbours' edges live.
    MARGIN = 0.15

    def detect(self, cell):
        sun_ratio, moon_ratio = self.scores(cell)

        sun = sun_ratio >= self.MIN_RATIO
        moon = moon_ratio >= self.MIN_RATIO

        if sun and moon:
            raise ValueError(
                f"Ambiguous cell: sun={sun_ratio:.3f} moon={moon_ratio:.3f}"
            )

        if sun:
            return Symbol.SUN

        if moon:
            return Symbol.MOON

        return Symbol.EMPTY

    def scores(self, cell):
        """Returns (sun_ratio, moon_ratio) over the central part of the cell."""
        height, width = cell.shape[:2]

        margin_y = int(height * self.MARGIN)
        margin_x = int(width * self.MARGIN)

        center = cell[margin_y:height - margin_y, margin_x:width - margin_x]

        hsv = cv2.cvtColor(center, cv2.COLOR_BGR2HSV)

        hue_ok = hsv[:, :, 1] >= self.MIN_SATURATION
        value_ok = hsv[:, :, 2] >= self.MIN_VALUE
        colored = hue_ok & value_ok

        hue = hsv[:, :, 0]

        sun_mask = colored & (hue >= self.SUN_HUE[0]) & (hue <= self.SUN_HUE[1])
        moon_mask = colored & (hue >= self.MOON_HUE[0]) & (hue <= self.MOON_HUE[1])

        total = center.shape[0] * center.shape[1]

        return sun_mask.sum() / total, moon_mask.sum() / total
