# -------------------------------------------------------------------
# Furuikeya Controller
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependancies
#=============
from colifrapy import Model
from twitter_client import TwitterClient
from saijiki import Saijiki
from protocol import Protocol

# Main Class
#=============
class Controller(Model):

	twitter = None
	saijiki = None
	protocol = None

	def __init__(self):

		# Annoucing
		self.log.header('main:title')

		# Registering Dependancies
		# self.saijiki = Saijiki()

		# Calling upon twitter API
		self.twitter = TwitterClient()
		tweet_generator = self.twitter.findTweets("frog");

		# Passing kigo and tweets to the protocol
		self.protocol = Protocol("moon", tweet_generator)