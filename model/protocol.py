# -*- coding: utf-8 -*- 

# -------------------------------------------------------------------
# Furuikeya Protocol
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependancies
#=============
import re
import string
import nltk

from lib.sylli import SylModule
from colifrapy import Model

from haiku import Haiku

# Main Class
#=============
class Protocol(Model):
    ''' The aim of the Protocol class is to create a valid Haiku from 
    the tweets it will receive. It will thus tokenize the tweets, counting
    their syllable and form the final haiku. '''

    # Properties
    #------------
    syl = None
    kigo = None
    tweets = None
    haiku = None

    verses_length = [5, 7, 5]
    verses_offset = 1

    sentence_detector = None

    # Tweet Filters
    filters = [
        # Retweets
        lambda t: True if re.search(r'\bRT\b', t) is None else False
        # Empty
        ,lambda t: t.strip() != ''
        # Mad Hashtaggers
        ,lambda t: t.count('#') < 4
    ]

    # Tweet Cleaners
    cleaners = [
        # Dropping special characters
        lambda t: re.sub(re.compile('[^'+string.printable+']'), '', t)
        # Dropping urls, hashtags and addressing
        ,lambda t: re.sub(r'\bhttp://.*\b|#|@[^ ]?|&.+?;', '', t)
        # Final Strip
        ,lambda t: t.rstrip().strip()
    ]

    # Constructor
    #------------
    def __init__(self, kigo, tweets=None):
        self.syl = SylModule(self.settings.sonorities)
        self.kigo = kigo
        self.tweets = tweets
        self.haiku = Haiku()

        # Initializing sentence tokenizer
        self.sentence_detector = nltk.data.load(self.settings.pickle)

        # Launching Protocol Loop
        for tweet in self.tweets:

            # Filtering and Cleansing
            if self.filterTweet(tweet):
                tweet = self.cleanTweet(tweet)

            # Tokenization
            print tweet
            tokens = self.sentence_detector.tokenize(tweet)
            self.isHaikuMaterial(tokens)

    # Methods
    #---------
    def filterTweet(self, tweet):
        for filter in self.filters:
            if not filter(tweet):
                return False
        return True

    def cleanTweet(self, tweet):
        for cleaner in self.cleaners:
            tweet = cleaner(tweet)
        return tweet

    def isHaikuMaterial(self, tokens):
        # Check la taille -> split en sous phrase
        # si c'est bon on remplit et on check la présence du kigo absolue
        for sentence in tokens:
            for semi_sentence in sentence.split(','):
                print nltk.word_tokenize(semi_sentence)
            
            # test = reduce(self.countSyllables, nltk.word_tokenize(sentence))

        pass

    # Helpers
    #---------
    def countSyllables(self, word, dict=None):
        return len(self.syl.syllabify(word).split('.'))



