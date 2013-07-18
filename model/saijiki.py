# -------------------------------------------------------------------
# Saijiki Abstraction
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependancies
#=============
import random
import codecs
from colifrapy import Model

# Main Class
#=============
class Saijiki(Model):
	''' The Saijiki class read the sajiki file and provides some
	generic methods to get random kigos from it '''

	kigo_list = None

	# Constructor
	def __init__(self):

		# Announcing
		self.log.write('saijiki:open')

		# Setting the kigo list
		with codecs.open(self.settings.saijiki, 'r') as sf:
			lines = sf.readlines()
		self.kigo_list = [i.rstrip() for i in lines if i.rstrip() != '']
		if len(self.kigo_list) == 0:
			self.log.write('saijiki:empty')
			self.kigo_list.append('moon')

	# Get random kigo
	def getRandomKigo(self):
		return random.choice(self.kigo_list)