# Dependancies


# Class Definition
class Tweet :
	''' Abstraction class for a tweet. '''

	# Constructor
	def __init__(self, json_data=False) :

		# If the json_data is given, we run the decode function immediatly
		if json_data != False :
			self.decode(json_data)


	# Decode the tweet from its json counterpart
	def decode(self, json_data) :

		# Informations about tweet
		self.language = json_data['iso_language_code']
		self.text = json_data['text']

		# Shortened language test
		if self.language != 'en' :
			self.is_english = False
		else :
			self.is_english = True

	# Dump the tweet
	def dump(self) :
		print('\n')
		print(self.text)
		print('\n')