class CellExtractor:

	def extract(self, board_image):
		height, width = board_image.shape[:2]

		cell_width = width // 6
		cell_height = height // 6

		cells = []

		for row in range(6):
			cell_row = []

			for col in range(6):
				x1 = col * cell_width
				y1 = row * cell_height

				x2 = x1 + cell_width
				y2 = y1 + cell_height

				cell = board_image[y1:y2, x1:x2]

				cell_row.append(cell)

			cells.append(cell_row)

		return cells