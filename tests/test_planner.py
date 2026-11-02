import unittest

from automation.planner import clicks_needed, plan_clicks
from automation.screen import Capture
from tango.board import Board
from tango.enums import Symbol

E, S, M = Symbol.EMPTY, Symbol.SUN, Symbol.MOON


class TestClicks(unittest.TestCase):
    def test_click_cycle_is_empty_sun_moon_empty(self):
        self.assertEqual(clicks_needed(E, S), 1)
        self.assertEqual(clicks_needed(E, M), 2)
        self.assertEqual(clicks_needed(S, M), 1)
        self.assertEqual(clicks_needed(M, S), 2)
        self.assertEqual(clicks_needed(M, E), 1)
        self.assertEqual(clicks_needed(S, E), 2)

    def test_nothing_to_do_when_already_right(self):
        for symbol in (E, S, M):
            self.assertEqual(clicks_needed(symbol, symbol), 0)

    def test_plan_skips_cells_that_are_already_right(self):
        current, solution = Board(), Board()

        current.set_cell(0, 0, S)
        solution.set_cell(0, 0, S)
        solution.set_cell(0, 1, M)
        solution.set_cell(5, 5, S)
        current.set_cell(5, 5, M)

        self.assertEqual(plan_clicks(current, solution), [(0, 1, 2), (5, 5, 2)])


class TestScreenMapping(unittest.TestCase):
    def test_plain_screen(self):
        self.assertEqual(Capture(None, 0, 0, 1).to_screen(120, 80), (120, 80))

    def test_second_monitor_offset(self):
        self.assertEqual(Capture(None, 1920, 0, 1).to_screen(100, 50), (2020, 50))

    def test_retina_screenshot_is_twice_the_mouse_units(self):
        self.assertEqual(Capture(None, 0, 0, 2).to_screen(400, 200), (200, 100))


if __name__ == "__main__":
    unittest.main()
