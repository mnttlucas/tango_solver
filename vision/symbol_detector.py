from enum import Enum

import cv2

class CellContent(Enum):
	EMPTY = 0
	SUN = 1
	MOON = 2

class SymbolDetector:

	def __init__(self):
		self.sun_template = cv2.imread("assets/templates/sun.png")
		self.moon_template = cv2.imread("assets/templates/moon.png")
		self.empty_template = cv2.imread("assets/templates/empty.png")

	def detect(self, cell):
		sun_score = self._compute_score(cell, self.sun_template)
		moon_score = self._compute_score(cell, self.moon_template)
		empty_score = self._compute_score(cell, self.empty_template)

		best_score = max(sun_score, moon_score,	empty_score)

		print(f"sun={sun_score:.3f} " f"moon={moon_score:.3f} "	f"empty={empty_score:.3f}")

		if best_score < 0.3:
			raise ValueError(f"Unknown symbol : " f"sun={sun_score:.3f} " f"moon={moon_score:.3f} " f"empty={empty_score:.3f}")

		if best_score == sun_score:
			return CellContent.SUN

		if best_score == moon_score:
			return CellContent.MOON

		return CellContent.EMPTY

	def _compute_score(self, image, template):
		result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

		return result[0][0]