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

        # Setting Twitter
        self.twitter = Twitter()

        # Setting the haiku
        self.haiku = Haiku()

        # Getting a kigo from the saijiki
        saijiki = Saijiki()
        self.kigo = saijiki.getRandomKigo()

        # Dev override
        self.kigo = "moon"

    # Creating one Haiku
    def generateHaiku(self) :

        # Getting the tweets
        tweets = self.twitter.getTweetsByHashtag(self.kigo)

        # Dumping the tweets
        for t in tweets :
            self.analyseTweet(t)
            t.dump()

    # Checking if a possible verse exists within the tweet
    def analyseTweet(self, tweet) :

        # A sentence will be until the second hashtag
        sentence = re.sub("#", "", tweet.text, 1)
        sentence = re.findall("[^#,-,;,.,\,]*[#,-,;,.,\,]{1}", sentence)
        #if sentence is not None :
            #print(sentence)
