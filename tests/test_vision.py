import unittest
from pathlib import Path

import cv2
import numpy as np

from tango.constraints import ConstraintType
from tango.enums import Symbol
from vision.board_reader import BoardNotFound, BoardReader

ASSETS = Path(__file__).resolve().parent.parent / "assets"

E, S, M = Symbol.EMPTY, Symbol.SUN, Symbol.MOON
EQ, DIFF = ConstraintType.EQUAL, ConstraintType.DIFFERENT

# What is on each screenshot (light mode), read by eye.
EXPECTED = {
    "screenshot-01.png": (
        [[E, E, E, M, M, S],
         [E, E, E, M, E, M],
         [E, E, E, S, M, S],
         [E] * 6, [E] * 6, [E] * 6],
        {((3, 0), (4, 0), EQ), ((3, 1), (3, 2), DIFF),
         ((4, 2), (5, 2), EQ), ((5, 0), (5, 1), EQ)},
    ),
    "screenshot-02.jpg": (
        [[M, E, E, E, E, M],
         [E, M, E, E, M, E],
         [E] * 6, [E] * 6,
         [E, S, E, E, M, E],
         [S, E, E, E, E, S]],
        {((2, 2), (2, 3), DIFF), ((2, 2), (3, 2), EQ),
         ((2, 3), (3, 3), DIFF), ((3, 2), (3, 3), EQ)},
    ),
    "solved-example.jpg": (
        [[S, M, M, S, S, M],
         [S, M, S, S, M, M],
         [M, S, S, M, M, S],
         [S, S, M, M, S, M],
         [M, M, S, S, M, S],
         [M, S, M, M, S, S]],
        {((3, 3), (4, 3), DIFF), ((4, 3), (5, 3), DIFF), ((4, 5), (5, 5), EQ),
         ((5, 3), (5, 4), DIFF), ((5, 4), (5, 5), EQ)},
    ),
}


def summarize(board):
    return (
        board.grid,
        {(c.pos1, c.pos2, c.constraint_type) for c in board.constraints},
    )


def load(name):
    image = cv2.imread(str(ASSETS / name))
    assert image is not None, name
    return image


class TestReadScreenshots(unittest.TestCase):
    def test_each_screenshot_is_read_correctly(self):
        for name, (grid, constraints) in EXPECTED.items():
            with self.subTest(name):
                board = BoardReader().read(load(name)).board
                self.assertEqual(summarize(board), (grid, constraints))


class TestFullScreenScenes(unittest.TestCase):
    """The board must be found wherever it is on a bigger screen."""

    def scene(self, name, scale, offset, background):
        image = load(name)
        image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        canvas = np.full((1080, 1920, 3), background, np.uint8)
        x, y = offset
        canvas[y:y + image.shape[0], x:x + image.shape[1]] = image

        return canvas

    def test_board_found_at_several_scales_and_positions(self):
        cases = [
            ("screenshot-01.png", 1.0, (300, 200), 255),
            ("screenshot-01.png", 0.8, (900, 100), 70),
            ("screenshot-02.jpg", 0.4, (100, 50), 255),
            ("screenshot-02.jpg", 0.35, (1000, 20), 40),
            ("solved-example.jpg", 0.35, (800, 200), 128),
            ("solved-example.jpg", 0.4, (30, 10), 200),
        ]

        for name, scale, offset, background in cases:
            with self.subTest(name=name, scale=scale):
                board = BoardReader().read(self.scene(name, scale, offset, background)).board
                self.assertEqual(summarize(board), EXPECTED[name])

    def test_geometry_follows_the_board(self):
        """Cell centers must move and scale with the board (they get clicked)."""
        reference = BoardReader().read(load("screenshot-02.jpg")).geometry

        scale, offset = 0.4, (500, 50)
        reading = BoardReader().read(self.scene("screenshot-02.jpg", scale, offset, 255))

        tolerance = 0.1 * reading.geometry.cell_size

        for row, col in [(0, 0), (2, 3), (5, 5)]:
            ref_x, ref_y = reference.cell_center(row, col)
            x, y = reading.geometry.cell_center(row, col)

            self.assertLess(abs(x - (offset[0] + scale * ref_x)), tolerance)
            self.assertLess(abs(y - (offset[1] + scale * ref_y)), tolerance)

    def test_no_board_in_a_blank_screen(self):
        blank = np.full((1080, 1920, 3), 255, np.uint8)

        with self.assertRaises(BoardNotFound):
            BoardReader().read(blank)

    def test_no_board_in_noise(self):
        noise = np.random.default_rng(1).integers(0, 255, (1080, 1920, 3), dtype=np.uint8)

        with self.assertRaises(BoardNotFound):
            BoardReader().read(noise)


if __name__ == "__main__":
    unittest.main()
