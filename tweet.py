# Dependancies
from string import ascii_letters, digits

# Class Definition
class Tweet :
	''' Abstraction class for a tweet. '''

	# Constructor
	def __init__(self, json_data=False) :

		# Kept characters
		self.kept_characters = [" ", "-", "_", "@", "#"]

		# Removed elements
		self.removed_elements = ["RT"]

		# If the json_data is given, we run the decode function immediatly
		if json_data != False :
			self.decode(json_data)


	# Decode the tweet from its json counterpart
	def decode(self, json_data) :

		# Tweet Text - Removing any non alphadecimal character
		self.text = json_data['text']
			# Keeping only alphanumeric and such
		self.text = "".join([ch for ch in self.text if ch in (ascii_letters + digits + ''.join(self.kept_characters))])
			# Removing annoying parts
		for removed_element in self.removed_elements :
			self.text = self.text.replace(removed_element, '')

		# Trimming
			self.text = self.text.strip()

		# Shortened language test
		self.language = json_data['iso_language_code']
		if self.language != 'en' :
			self.is_english = False
		else :
			self.is_english = True

	# Dump the tweet
	def dump(self) :
		print('\n')
		print(self.text)
		print('\n')