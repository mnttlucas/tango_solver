from tango.enums import Symbol
from tango.rules import (validate_rows, validate_columns, validate_adjacency, validate_constraints, validate_final_columns, validate_final_rows)

class Board:
	def __init__(self, size = 6):
		self.size = size
		self.grid = [[Symbol.EMPTY for _ in range(self.size)] for _ in range(self.size)]
		self.constraints = []

	def __str__(self):
		symbols = {Symbol.EMPTY: ".", Symbol.SUN: "S", Symbol.MOON: "M"}
		lines = []

		for row in self.grid:
			lines.append(" ".join(symbols[cell] for cell in row))

		return "\n".join(lines)

	def get_cell(self, row, col):
		return self.grid[row][col]

	def set_cell(self, row, col, symbol):
		self.grid[row][col] = symbol

	def get_row(self, row):
		return self.grid[row]

	def get_column(self, col):
		return [self.grid[row][col] for row in range(self.size)]

	def add_constraint(self, constraint):
		self.constraints.append(constraint)

	def is_valid(self):
		return(validate_rows(self) and validate_columns(self) and validate_adjacency(self) and validate_constraints(self))

	def is_complete(self):
		for row in self.grid:
			if Symbol.EMPTY in row:
				return False
		return True

	def is_solved(self):
		return(self.is_complete() and self.is_valid() and validate_final_columns(self) and validate_final_rows(self))