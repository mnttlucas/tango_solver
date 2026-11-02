import unittest

from vision.image_loader import load_image

class TestImageLoading(unittest.TestCase):
    def test_phone_screenshot_loads(self):
        image = load_image("assets/screenshot-03.jpg")
        self.assertIsNotNone(image)

    def test_pc_screenshot_loads(self):
        image = load_image("assets/screenshot-01.png")
        self.assertIsNotNone(image)

    def test_dark_screenshot_loads(self):
        image = load_image("assets/screenshot-04.png")
        self.assertIsNotNone(image)