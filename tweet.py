# Dependancies
from string import ascii_letters
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
			# Removing RT and http links and addressing
		self.text = re.sub("https?://[^ ]*|@[^ ]*", "", self.text)
			# Keeping only alphanumeric and such
		self.text = "".join([ch for ch in self.text if ch in (ascii_letters + ''.join(self.kept_characters))])
			# Trimming
		self.text = self.text.strip()

	# Analyse of the tweet to see if it proves good material for a Haiku
	# Hook for more rules later
	def isHaikuMaterial(self) :

		# If the tweet contains more than two hashtags we drop it for being a glory seeker
		if self.text.count('#') > 6 :
			return False

		# If retweet, we drop, just to be sure not to have twice the same verse
		if self.text.count('RT') > 0 :
			return False

		return True

	# Dump the tweet
	def dump(self) :
		print('\n')
		print(self.text)
		print('\n')