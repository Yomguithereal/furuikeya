# Dependancies
import urllib.request
import json
from tweet import Tweet

# Class Definition
class Twitter :
	''' The Twitter Class represents the inteface of furuikeya
	with Twitter API. Its aim is to fetch the tweets by hashtags
	from the saijiki '''

	# Constructor
	def __init__(self) :
		self.base_url = 'http://search.twitter.com/search.json?q=%23'
		self.next_url = ''

	# Get the tweets by hashtag
	def getTweetsByHashtag(self, hashtag) :
		tweets = self.get_url(self.base_url+hashtag)

		for tweet in tweets :
			print(self.next_url)


	# Utilities
	def get_url(self, url) :
		response = urllib.request.urlopen(url)
		json_data = json.loads(response.read().decode('utf-8'))

		# Keeping the next url to get
		self.next_url = json_data['next_page']

		return json_data['results']

	def dump_tweet(self, json_tweet) :
		print(json_tweet)