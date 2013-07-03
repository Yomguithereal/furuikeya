# -------------------------------------------------------------------
# Furuikeya Twitter Client
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependancies
#=============
from twitter import Twitter, OAuth
from colifrapy import Model
from pprint import pprint

# Main Class
#=============
class TwitterClient(Model):

	# Properties
	t = None
	opts = {
		'lang' : 'en',
		'result_type' : 'recent',
		'count' : '50',
		'include_entities' : 'false'
	}

	# Constructor
	def __init__(self):

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
		self.log.write('twitter:open', variables={'kigo' : kigo})

		self.opts["q"] = kigo+'%20-RT'
		search = self.t.search.tweets(**self.opts)
		for tweet in search['statuses']:
			yield tweet['text'].encode('utf-8', 'ignore')
