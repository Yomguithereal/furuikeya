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
		with open(self.settings.saijiki, 'r') as sf:
			lines = sf.readlines()
		self.kigo_list = [i.rstrip() for i in lines if i.rstrip() != '']

	# Get random kigo
	def getRandomKigo(self):
		return random.choice(self.kigo_list)