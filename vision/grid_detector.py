import cv2
import numpy as np


class GridDetector:
    """Finds the 6x6 Tango board anywhere in an image (full screen included).

    Strategy: propose square-ish boxes from weak edges, then keep the one whose
    inner structure really looks like a grid, i.e. strong edges on the 5
    interior lines of each axis and weak edges at the cell centers.
    The check does not depend on colors, so it is not tied to light mode.
    """

    GRID_SIZE = 6
    MIN_SIDE = 150
    MIN_SCORE = 0.45
    MIN_CONSISTENCY = 0.1
    COLOR_SATURATION = 70

    def detect(self, image):
        """Returns (x, y, w, h) of the board, or None if no board is found."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        grad_x = np.abs(cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3))
        grad_y = np.abs(cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3))

        # Grid lines are pale and nearly colorless. Sun, moon and sign pixels
        # are strongly colored and their outlines are far stronger than the
        # lines, so they would hijack the fit: ignore every edge touching them.
        colored = self._colored_mask(image)
        grad_x[colored] = 0
        grad_y[colored] = 0

        best = None

        for x, y, side in self._candidates(gray):
            fit = self._fit(grad_x, grad_y, x, y, side)

            if fit is None:
                continue

            x, y, side, score = fit

            if score < self.MIN_SCORE:
                continue

            # The whole board has to be visible.
            if x < 0 or y < 0 or x + side > gray.shape[1] or y + side > gray.shape[0]:
                continue

            # Prefer the largest valid grid: small periodic patterns inside a
            # cell can score high, but they are never bigger than the board.
            if best is None or side > best[2]:
                best = (x, y, side, score)

        if best is None:
            return None

        x, y, side, _ = best
        return (x, y, side, side)

    def _colored_mask(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = (hsv[:, :, 1] > self.COLOR_SATURATION).astype(np.uint8)

        # Also cover the anti-aliased rim of each colored shape.
        mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))

        return mask.astype(bool)

    def crop(self, image):
        rect = self.detect(image)

        if rect is None:
            raise ValueError("No Tango board found in the image")

        x, y, w, h = rect
        return image[y:y + h, x:x + w]

    def _candidates(self, gray):
        height, width = gray.shape

        # Very low thresholds on purpose: board lines are pale beige on white.
        edges = cv2.Canny(gray, 8, 24)
        edges = cv2.dilate(edges, np.ones((3, 3), np.uint8))

        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        seen = set()

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if w < self.MIN_SIDE or h < self.MIN_SIDE:
                continue

            if not 0.93 <= w / h <= 1.07:
                continue

            if w > 0.98 * width and h > 0.98 * height:
                continue

            seen.add((x, y, (w + h) // 2))

        return seen

    def _fit(self, grad_x, grad_y, x, y, side):
        """Fits the 6x6 line comb around a rough box.

        Each axis is fitted on its own (position and cell pitch), exhaustively
        over a small neighbourhood, then the two fits must agree on the pitch.
        Returns (x, y, side, score) or None.
        """
        height, width = grad_x.shape

        inner = int(side * 0.05)

        rows = slice(max(0, y + inner), min(height, y + side - inner))
        cols = slice(max(0, x + inner), min(width, x + side - inner))

        # Vertical lines show up in the horizontal gradient, and vice versa.
        profile_x = self._continuity(grad_x[rows, :], axis=0)
        profile_y = self._continuity(grad_y[:, cols], axis=1)

        fit_x = self._fit_axis(profile_x, x, side)
        fit_y = self._fit_axis(profile_y, y, side)

        if fit_x is None or fit_y is None:
            return None

        start_x, pitch_x, score_x = fit_x
        start_y, pitch_y, score_y = fit_y

        if abs(pitch_x - pitch_y) > 0.02 * max(pitch_x, pitch_y):
            return None

        pitch = (pitch_x + pitch_y) / 2

        return (
            int(round(start_x)),
            int(round(start_y)),
            int(round(pitch * self.GRID_SIZE)),
            min(score_x, score_y),
        )

    def _continuity(self, gradient, axis):
        """Edge strength per position, counting only edges that run all along.

        The region is cut in 6 bands across the lines' direction, and each
        position keeps its third weakest band. A grid line must show in at
        least 4 bands (it can fade where it separates two beige locked cells),
        while sun/moon outlines are only in the bands that hold a glyph and a
        column never holds more than 3 identical symbols.
        """
        n = self.GRID_SIZE

        if axis == 0:
            bands = np.array_split(gradient, n, axis=0)
            means = np.stack([band.mean(axis=0) for band in bands])
        else:
            bands = np.array_split(gradient, n, axis=1)
            means = np.stack([band.mean(axis=1) for band in bands])

        return np.sort(means, axis=0)[2]

    def _fit_axis(self, profile, approx_start, approx_side):
        """Best (start, pitch, score) of the interior-line comb on one axis."""
        n = self.GRID_SIZE
        length = len(profile)

        # A thin line gives two close edges in |gradient|; blur merges them
        # into a single peak sitting right on the line.
        sigma = max(1.5, approx_side / n * 0.012)
        smooth = cv2.GaussianBlur(
            profile.astype(np.float32).reshape(1, -1), (0, 0), sigma
        ).ravel()

        margin = max(6, int(approx_side * 0.04))

        starts = np.arange(approx_start - margin, approx_start + margin + 1)
        line_index = np.arange(1, n)
        center_index = np.arange(n) + 0.5

        best = None

        for side in range(approx_side - margin, approx_side + margin + 1):
            pitch = side / n

            line_pos = np.rint(starts[:, None] + pitch * line_index[None, :]).astype(int)
            center_pos = np.rint(starts[:, None] + pitch * center_index[None, :]).astype(int)

            inside = (
                (line_pos.min(axis=1) >= 0) & (line_pos.max(axis=1) < length)
                & (center_pos.min(axis=1) >= 0) & (center_pos.max(axis=1) < length)
            )

            if not inside.any():
                continue

            lines = smooth[np.clip(line_pos, 0, length - 1)]
            centers = smooth[np.clip(center_pos, 0, length - 1)]

            line_mean = lines.mean(axis=1)
            center_mean = centers.mean(axis=1)

            # Every interior line must be present, not just a couple of them.
            present = lines.min(axis=1) >= self.MIN_CONSISTENCY * (lines.max(axis=1) + 1e-6)

            # Fit by line energy, which has a sharp maximum at the true grid.
            fit = np.where(present & inside, line_mean, -1.0)

            index = int(np.argmax(fit))

            if fit[index] > 0 and (best is None or fit[index] > best[0]):
                contrast = (line_mean[index] - center_mean[index]) / (
                    line_mean[index] + center_mean[index] + 1e-6
                )
                best = (float(fit[index]), float(starts[index]), pitch, float(contrast))

        if best is None:
            return None

        return best[1], best[2], best[3]
