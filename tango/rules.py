from tango.constraints import ConstraintType
from tango.enums import Symbol

def validate_rows(board):
	max_symbols = board.size // 2

	for row in range(board.size):
		if(not validate_balance(board.get_row(row), max_symbols)):
			return False
	return True

def validate_columns(board):
	max_symbols = board.size // 2

	for col in range(board.size):
		if(not validate_balance(board.get_column(col), max_symbols)):
			return False
	return True

def validate_balance(values, max_symbols):
	return(values.count(Symbol.SUN) <= max_symbols and values.count(Symbol.MOON) <= max_symbols)

def validate_adjacency(board):
	for idx in range(board.size):
		if(not (validate_line_adjacency(board.get_row(idx)) and validate_line_adjacency(board.get_column(idx)))):
			return False
	return True

def validate_line_adjacency(values):
	for i in range(len(values) - 2):
		current = values[i]

		if(current == Symbol.EMPTY):
			continue

		if(values[i + 1] == current and values[i + 2] == current):
			return False
	return True

def validate_constraints(board):
	for constraint in board.constraints:
		if not validate_constraint(board, constraint):
			return False
	return True

def validate_constraint(board, constraint):
	row1, col1 = constraint.pos1
	row2, col2 = constraint.pos2
	value1 = board.get_cell(row1, col1)
	value2 = board.get_cell(row2, col2)

	if value1 == Symbol.EMPTY or value2 == Symbol.EMPTY:
		return True
	
	if constraint.constraint_type == ConstraintType.EQUAL:
		return value1 == value2
	else:
		return value1 != value2

def validate_final_rows(board):
	expected_count = board.size // 2

	for row_idx in range(board.size):
		values = board.get_row(row_idx)

		if(values.count(Symbol.SUN) != expected_count or values.count(Symbol.MOON) != expected_count):
			return False
		
	return True

def validate_final_columns(board):
	expected_count = board.size // 2

	for col_idx in range(board.size):
		values = board.get_column(col_idx)

		if(values.count(Symbol.SUN) != expected_count or values.count(Symbol.MOON) != expected_count):
			return False

	return True