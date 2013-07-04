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
	kigo_in_verses = False
	kireji_position = None
	kireji = None
	kireji_list = [';', ',', ' -']
	verses = ['', '', '']
	short_verses = False
	long_verse = False
	string = ''

	# Constructor
	def __init__(self, kigo) :

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
			self.kigo_in_verses = True
		return self.kigo_in_verses

	def _lastVerse(self):
		return len([i for i in self.verses if i == '']) == 1

	def setLongVerse(self, verse):
		
		# Verification
		if self.verses[1] != '':
			return False
		if not self._checkKigoInVerse(verse) and self._lastVerse():
			return False
		
		# Setting
		self.verses[1] = verse.strip().rstrip()


	def setShortVerse(self, verse):

		# Verifications
		if self.shortVersesComplete():
			return False
		if not self._checkKigoInVerse(verse) and self._lastVerse():
			return False

		# Setting
		if self.verses[0] == '':
			self.verses[0] = verse.strip().rstrip()
		else:
			self.verses[2] = verse.strip().rstrip()


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

	def shortVersesComplete(self):
		return len([i for i in [self.verses[0], self.verses[2]] if i == '']) == 0