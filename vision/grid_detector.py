import cv2


class GridDetector:

	def detect(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		_, thresh = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)

		contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		best_rect = None
		best_area = 0

		image_area = (image.shape[0] * image.shape[1])

		for contour in contours:
			area = cv2.contourArea(contour)

			if area < 5000:
				continue

			if area > image_area * 0.8:
				continue

			x, y, w, h = cv2.boundingRect(contour)

			aspect_ratio = w / h

			if not 0.9 <= aspect_ratio <= 1.1:
				continue

			if area > best_area:
				best_area = area
				best_rect = (x,	y, w, h)

		return best_rect

	def crop(self, image):
		x, y, w, h = self.detect(image)
		return image[y:y + h, x:x + w]