# Dependancies
from string import ascii_letters, digits
import re

# Class Definition
class Tweet :
	''' Abstraction class for a tweet. '''

	# Constructor
	def __init__(self, json_data=False) :

		# Kept characters
		self.kept_characters = [" ", "-", "_", "@", "#"]

		# If the json_data is given, we run the decode function immediatly
		if json_data != False :
			self.decode(json_data)


	# Decode the tweet from its json counterpart
	def decode(self, json_data) :

		# Tweet Text
		self.text = json_data['text']
			# Removing RT and http links
		self.text = re.sub("RT|https?://[^ ]*", "", self.text)
			# Keeping only alphanumeric and such
		self.text = "".join([ch for ch in self.text if ch in (ascii_letters + digits + ''.join(self.kept_characters))])
			# Trimming
		self.text = self.text.strip()

		# Shortened language test
		self.language = json_data['iso_language_code']
		if self.language != 'en' :
			self.is_english = False
		else :
			self.is_english = True

	# Analyse of the tweet to see if it proves good material for a Haiku
	def isHaikuMaterial(self) :

		# If the tweet is not in English, we drop it. Harsh isn't it?
		if not self.is_english :
			return False

		# If the tweet contains more than two hashtags we drop it for being a glory seeker
		if self.text.count('#') > 10 :
			return False

		return True

	# Dump the tweet
	def dump(self) :
		print('\n')
		print(self.text)
		print('\n')