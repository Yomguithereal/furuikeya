# Dependancies
from haiku import Haiku
from saijiki import Saijiki
from twitter import Twitter
from lib.sylli.sylli import SylModule
import re

# Class Definition
class Furuikeya :
	''' Main class of the furuikeya protocol. Provides
	abstraction methods to generate Haikus from Twitter
	using the selected kigo. '''

	# Constructor
	def __init__(self) :

		# Setting the syllable variables
		self.syllable_offset = 1
		self.short_verse_size = 5
		self.long_verse_size = 7

		self.syl = SylModule()
		self.syl.load_conf('config/sonority.txt')

		# Setting Twitter
		self.twitter = Twitter()

		# Setting the haiku
		self.haiku = Haiku()

		# Getting a kigo from the saijiki
		saijiki = Saijiki()
		self.kigo = saijiki.getRandomKigo()

		# Dev override
		self.kigo = "france"

	# Creating one Haiku
	def generateHaiku(self) :

		# Getting the tweets
		tweets = self.twitter.getTweetsByHashtag(self.kigo)

		# Dumping the tweets
		for t in tweets :
			self.analyseTweet(t)

		# Checking if the Haiku is complete
		if self.haiku.is_complete() :

			# Displaying the generated haiku
			print("\n")
			print(self.haiku.output())
			print("\n")
		else :

			# Not enough material, we relaunch the function
			self.generateHaiku()

	# Checking if a possible verse exists within the tweet
	# If a verse exists, it associates it to the haiku
	def analyseTweet(self, tweet) :

		# A sentence will be until the second hashtag
		sentence = re.sub("#", "", tweet.text, 1)
		sentence = re.findall("^[^#]{1}[^#,-,;,.]*", sentence)

		# Checking the sentences to find verses
		if sentence[0] is not None :
			sentence = sentence[0].strip()
			count = self.countSyllables(sentence)

			# If short verse
			if count >= self.short_verse_size - self.syllable_offset and count <= self.short_verse_size + self.syllable_offset :
				if self.haiku.first_verse == '' :
					self.haiku.first_verse = sentence
				else :
					if self.haiku.third_verse == '' :
						self.haiku.third_verse = sentence

			# If long verse
			elif count >= self.long_verse_size - self.syllable_offset and count <= self.long_verse_size + self.syllable_offset :
				if self.haiku.second_verse == '' :
					self.haiku.second_verse = sentence

		return True


	# Checking syllable possibility
	def countSyllables(self, string) :

		# Cutting the string into words
		words = string.split(" ")

		# Checking syllables
		count = 0
		for word in words :
			syllabified = self.syl.syllabify(word)
			count += len(syllabified.split('.'))

		return count











