from enum import Enum

class ConstraintType(Enum):
	DIFFERENT = 0
	EQUAL = 1

class Constraint:
	def __init__(self, pos1, pos2, constraint_type):
		self.pos1 = pos1
		self.pos2 = pos2
		self.constraint_type = constraint_type