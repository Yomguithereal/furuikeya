# Dependancies
import os
import random

# Class Definition
class Saijiki :
	''' The Saijiki class represents the interaction with the saijiki.txt
	config file. Its aim is to select a kigo from it in order to direct
	the Haiku generation aftewards '''

	# Constructor
	def __init__(self, path="config/saijiki.txt") :

		# Saijiki config path
		self.saijiki_path = path

		# Setting the kigo list
		file_lines = list(open(self.saijiki_path, 'r'))
		self.kigo_list = [i.rstrip() for i in file_lines]


	# Getting a random kigo
	def getRandomKigo(self) :
		return random.choice(self.kigo_list)



