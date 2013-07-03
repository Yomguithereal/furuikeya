# -------------------------------------------------------------------
# Haiku Abstraction
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependancies
#=============
import random

# Main Class
#=============
class Haiku:
	''' The Haiku class is just a mere abstraction of what
	furuikeya will be able to output. It handles its verses,
	its kigo and its kireji'''

	# Properties
	kigo = None
	kigo_in_verse = False
	kireji_position = None
	kireji = None
	kireji_list = [';', ',', ' -']
	verses = ['', '', '']
	string = ''

	# Constructor
	def __init__(self, kigo="moon") :

		# Kireji Position
		#	0 = between first and second verse
		#	1 = between second and third verse
		self.kireji_position = random.randint(0, 1)

		# Possible kireji
		self.kireji = random.choice(self.kireji_list)

		# Kigo
		self.kigo = kigo

	# Printing
	def __repr__(self):
		if self.isComplete():
			return self.output()
		else:
			return 'Haiku is not complete'

	# Output method
	def output(self) :
		if self.string.strip() == '':
			for nb, verse in enumerate(self.verses):
				self.string += verse
				if nb == self.kireji_position:
					self.string += self.kireji
				if nb < 2:
					self.string += '\n'
		return self.string

	# Completion
	def isComplete(self):
		return not reduce(lambda d,x: x.strip() == '', self.verses)
