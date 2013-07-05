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
    protocol = None
    haikus = []

    # Constructor
    #------------
    def __init__(self):

        # Annoucing
        self.log.header('main:title')

        # Registering Dependancies
        self.twitter = TwitterClient()

    # Methods
    #------------
    def generateHaiku(self, kigo):
        
        # Passing kigo and tweets to the protocol
        while self.protocol.procede(self.twitter.findTweets(kigo)) is False:
            self.log.write('controller:not_enough')

        # Haiku is complete
        self.haikus.append(self.protocol.haiku)
        print ''
        print self.protocol.haiku
        print ''

    def generateMultipleHaikus(self, kigo, number=1):

        # Initiating protocol
        self.protocol = Protocol(kigo)

        # Looping
        for i in range(number):
            self.generateHaiku(kigo)