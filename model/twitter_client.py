# -------------------------------------------------------------------
# Furuikeya Twitter Client
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependancies
#=============
import re
import random

from twitter import Twitter, OAuth
from colifrapy import Model
from pprint import pprint

# Main Class
#=============
class TwitterClient(Model):

	# Properties
	t = None
	twopts = {
		'lang' : 'en',
		'result_type' : 'recent',
		'count' : '100',
		'include_entities' : 'false'
	}

	# Constructor
	def __init__(self):

		# Announcing
		self.log.write('twitter:open')

		# Regsitering Oauth
		self.t = Twitter(auth=OAuth(
			self.settings.twitter['oauth_token'],
			self.settings.twitter['oauth_secret'],
			self.settings.twitter['consumer_key'],
			self.settings.twitter['consumer_secret']
		))

	# Find Tweets
	def findTweets(self, kigo):

		# Announcing
		self.log.write('twitter:fetch', variables={'kigo' : kigo})

		# Options
		self.twopts["q"] = kigo+'%20-RT'
		search = self.t.search.tweets(**self.twopts)

		# Setting the next page
		next_results = re.search(r'max_id=([^&]+)&', search['search_metadata']['next_results'])
		self.twopts['max_id'] = next_results.group(1)

		# Yielding
		random.shuffle(search['statuses'])
		for tweet in search['statuses']:
			yield tweet['text']