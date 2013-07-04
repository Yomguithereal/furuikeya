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

	# Properties
	twitter = None
	saijiki = None
	protocol = None

	# Constructor
    #------------
	def __init__(self):

		# Annoucing
		self.log.header('main:title')

		# Registering Dependancies
		# self.saijiki = Saijiki()

		# Calling upon twitter API
		kigo = 'frog'
		self.twitter = TwitterClient()

		# Passing kigo and tweets to the protocol
		self.protocol = Protocol(kigo)
		while self.protocol.procede(self.twitter.findTweets(kigo)) is False:
			self.log.write('controller:not_enough')

		# Haiku is complete
		print self.protocol.haiku

	# Methods
    #------------