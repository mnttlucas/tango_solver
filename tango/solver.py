from tango.enums import Symbol

class Solver:
	def solve(self, board):
		if board.is_solved():
			return True

		empty_cell = self.find_empty_cell(board)

		if empty_cell is None:
			return False

		row, col = empty_cell

		for symbol in (Symbol.SUN, Symbol.MOON):
			board.set_cell(row, col, symbol)

			if board.is_valid():
				if self.solve(board):
					return True

			board.set_cell(row, col, Symbol.EMPTY)

		return False

	def find_empty_cell(self, board):
		for row in range(board.size):
			for col in range(board.size):
				if board.get_cell(row, col) == Symbol.EMPTY:
					return (row, col)
		return None