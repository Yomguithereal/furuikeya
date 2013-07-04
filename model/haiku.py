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
	short_verses = False
	long_verse = False
	string = ''

	# Constructor
	def __init__(self, kigo=None) :

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

	# Setters
	def _checkKigoInVerse(self, verse):
		if verse.lower().count(self.kigo) > 0:
			self.kigo_in_verse = True
		return self.kigo_in_verse

	def _lastVerse(self):
		return len([i for i in self.verses if i == '']) == 1

	def setLongVerse(self, verse):
		if not self._checkKigoInVerse(verse) and self._lastVerse():
			return False
		if self.verses[1] == '':
			self.verses[1] = verse
		else:
			return False
		return True

	def setShortVerse(self, verse):
		if not self._checkKigoInVerse(verse) and self._lastVerse():
			return False
		if self.verses[0] == '':
			self.verses[0] = verse
		else:
			if self.verses[2] == '':
				self.verses[2] = verse
			else:
				return False
		return True


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
		return len([i for i in self.verses if i == '']) == 0