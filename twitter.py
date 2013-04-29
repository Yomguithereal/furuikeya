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
		self.base_url = 'http://search.twitter.com/search.json?lang=en&rpp=100&q=%23'
		self.next_url = ''

	# Get the tweets by hashtag
	def getTweetsByHashtag(self, hashtag) :

		# Checking if the next url is set
		if self.next_url == '' :
			json_tweets = self.get_url(self.base_url+hashtag)
		else :
			json_tweets = self.get_url(self.base_url+self.next_url)

		# Getting the tweets
		tweets = []
		for jt in json_tweets :
			tweet = Tweet(jt)

			# If the tweet is ok we keep it
			if tweet.isHaikuMaterial() :
				tweets.append(tweet)

		# Returning the tweets
		return tweets



	# Utilities
	def get_url(self, url) :
		print(url)
		response = urllib.request.urlopen(url)
		json_data = json.loads(response.read().decode('utf-8'))

		# Keeping the next url to get
		self.next_url = json_data['next_page']

		return json_data['results']