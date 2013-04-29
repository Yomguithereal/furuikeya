# Dependancies
import random

# Class Definition
class Haiku :
	''' The Haiku class is just a mere abstraction of what
	furuikeya will be able to output. It handles its verses,
	its kigo and its kireji'''

	# Constructor
	def __init__(self, kigo="moon") :

		# Kireji Position
		#	0 = between first and second verse
		#	1 = between second and third verse
		self.kireji_position = random.randint(0, 1)

		# Possible kireji
		self.kireji_list = [';', ',', '-']
		self.kireji = random.choice(self.kireji_list)

		# Verse
		self.first_verse = ''
		self.second_verse = ''
		self.third_verse = ''

		# Kigo
		self.kigo = kigo


	# Output method
	def output(self) :
		if self.kireji_position == 0 :
			haiku_string = self.first_verse + ' ' + self.kireji + '\n' + self.second_verse + '\n' + self.third_verse
		else :
			haiku_string = self.first_verse + '\n' + self.second_verse + ' ' + self.kireji + '\n' + self.third_verse

		return haiku_string.lower()

	# Checking the completion of the Haiku
	def is_complete(self) :
		if self.first_verse != '' and self.second_verse != '' and self.third_verse != '' :
			return True
		else :
			return False