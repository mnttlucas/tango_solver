import unittest
from pathlib import Path

from vision.image_loader import load_image

ASSETS = Path(__file__).resolve().parent.parent / "assets"


class TestImageLoading(unittest.TestCase):
    def test_phone_screenshot_loads(self):
        image = load_image(str(ASSETS / "screenshot-02.jpg"))
        self.assertIsNotNone(image)

    def test_pc_screenshot_loads(self):
        image = load_image(str(ASSETS / "screenshot-01.png"))
        self.assertIsNotNone(image)

    def test_dark_screenshot_loads(self):
        image = load_image(str(ASSETS / "screenshot-03.png"))
        self.assertIsNotNone(image)
