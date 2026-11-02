import copy
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import cv2

import play
from automation.screen import Capture
from tango.enums import Symbol
from tango.solver import Solver
from vision.board_reader import BoardReader

ASSETS = Path(__file__).resolve().parent.parent / "assets"

LOCKED = {(0, 0), (0, 5), (1, 1), (1, 4), (4, 1), (4, 4), (5, 0), (5, 5)}

# Fake monitor: not at the origin, and twice as many pixels as mouse units.
LEFT, TOP, SCALE = 1440, 120, 2.0


def _load_references():
    base = cv2.imread(str(ASSETS / "screenshot-02.jpg"))
    solved = cv2.imread(str(ASSETS / "solved-example.jpg"))

    base_reading = BoardReader().read(base)
    solved_reading = BoardReader().read(solved)

    return base, base_reading, solved, solved_reading.geometry


REFERENCES = _load_references()


class FakeGame:
    """A Tango page that reacts to clicks, seen through screenshots.

    Starts from screenshot-02 and redraws each free cell as empty, sun or moon
    by pasting cell images taken from the other screenshots.
    """

    def __init__(self, ignore_clicks=0):
        self.base, base_reading, solved, solved_geometry = REFERENCES
        self.geometry = base_reading.geometry
        self.state = [[Symbol.EMPTY] * 6 for _ in range(6)]
        self.ignore_clicks = ignore_clicks
        self.clicks = []

        for row, col in LOCKED:
            self.state[row][col] = base_reading.board.get_cell(row, col)

        self.glyphs = {
            Symbol.EMPTY: self.crop(self.base, self.geometry, 0, 1),
            Symbol.SUN: self.crop(solved, solved_geometry, 0, 3),
            Symbol.MOON: self.crop(solved, solved_geometry, 0, 1),
        }

    def inner(self, geometry, row, col):
        """Pixel box of the middle of a cell, away from borders and signs."""
        cell = geometry.cell_size
        x1 = int(geometry.x + (col + 0.2) * cell)
        y1 = int(geometry.y + (row + 0.2) * cell)
        size = int(cell * 0.6)
        return y1, y1 + size, x1, x1 + size

    def crop(self, image, geometry, row, col):
        y1, y2, x1, x2 = self.inner(geometry, row, col)
        return image[y1:y2, x1:x2].copy()

    def capture(self):
        image = self.base.copy()

        for row in range(6):
            for col in range(6):
                if (row, col) in LOCKED:
                    continue

                y1, y2, x1, x2 = self.inner(self.geometry, row, col)
                image[y1:y2, x1:x2] = self.glyphs[self.state[row][col]]

        return Capture(image, LEFT, TOP, SCALE)

    def grab(self, monitor=None):
        yield self.capture()

    def click(self, x, y, times=1, interval=0.15):
        # Back from mouse units to image pixels, then to a cell.
        px = (x - LEFT) * SCALE
        py = (y - TOP) * SCALE
        cell = self.geometry.cell_size

        col = int((px - self.geometry.x) // cell)
        row = int((py - self.geometry.y) // cell)

        self.clicks.append((row, col, times))

        if (row, col) in LOCKED or not (0 <= row < 6 and 0 <= col < 6):
            return

        if self.ignore_clicks > 0:
            self.ignore_clicks -= 1
            return

        for _ in range(times):
            self.state[row][col] = Symbol((self.state[row][col].value + 1) % 3)


def expected_solution():
    solution = copy.deepcopy(REFERENCES[1].board)
    Solver().solve(solution)
    return solution


class TestPlaySimulation(unittest.TestCase):
    def run_play(self, game, *extra):
        with mock.patch("play.screen.grab", game.grab), \
             mock.patch("play.screen.click", game.click), \
             mock.patch("play.time.sleep"), \
             tempfile.TemporaryDirectory() as debug_dir:
            play.main(["--wait", "0", "--debug-dir", debug_dir, *extra])

    def test_plays_a_whole_puzzle(self):
        game = FakeGame()
        self.run_play(game)

        solution = expected_solution()

        for row in range(6):
            for col in range(6):
                self.assertEqual(game.state[row][col], solution.get_cell(row, col), (row, col))

    def test_never_clicks_a_given_cell(self):
        game = FakeGame()
        self.run_play(game)

        clicked = {(row, col) for row, col, _ in game.clicks}
        self.assertFalse(clicked & LOCKED)

    def test_dry_run_does_not_click(self):
        game = FakeGame()
        self.run_play(game, "--dry-run")

        self.assertEqual(game.clicks, [])

    def test_missed_clicks_are_noticed_and_redone(self):
        game = FakeGame(ignore_clicks=3)
        self.run_play(game)

        solution = expected_solution()

        for row in range(6):
            for col in range(6):
                self.assertEqual(game.state[row][col], solution.get_cell(row, col), (row, col))


if __name__ == "__main__":
    unittest.main()
