# Dependancies
from haiku import Haiku
from saijiki import Saijiki
from twitter import Twitter

# Class Definition
class Furuikeya :
    ''' Main class of the furuikeya protocol. Provides a
    lot of abstraction methods to generate Haikus from Twitter
    using the selected kigo. '''

    # Constructor
    def __init__(self) :

        # Setting Twitter
        self.twitter = Twitter()

        # Getting a kigo from the saijiki
        saijiki = Saijiki()
        self.kigo = saijiki.getRandomKigo()

    # Creating one Haiku
    def generateHaiku(self) :

        # Getting the tweets
        tweets = self.twitter.getTweetsByHashtag(self.kigo)

        # Dumping the tweets
        for t in tweets :
            t.dump()