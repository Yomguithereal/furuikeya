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
        while self.protocol.procede(self.twitter.findTweets(kigo), kigo) is False:
            self.log.write('controller:not_enough')

        # Haiku is complete
        self.haikus.append(self.protocol.haiku)
        print ''
        print self.protocol.haiku
        print ''

    def generateMultipleHaikus(self, kigo=None, number=1):

        # Checking kigo
        if kigo is None:
            self.log.write('controller:kigo_not_given')
            saijiki = Saijiki()
            kigo = saijiki.getRandomKigo()

        # Initiating protocol
        self.protocol = Protocol()

        # Looping
        self.log.write('controller:number', variables={'nb' : number})
        for i in range(number):
            self.generateHaiku(kigo)

        self.log.write('main:end')

    def generateSaijikiHaikus(self, number=1):

        # Initializing saijiki
        self.log.write('controller:saijiki')
        saijiki = Saijiki()

        # Initiating protocol
        self.protocol = Protocol()

        # Looping
        for kigo in saijiki.kigo_list:
            for i in range(number):
                self.generateHaiku(kigo)

        self.log.write('main:end')