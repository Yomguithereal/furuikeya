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
    haiku = None
    verses_offset = 1

    sentence_detector = None
    punctuation_re = r'[“?!.,;:\-_/()\[\]{}`"]|\'\'|[0-9]'

    # Tweet Filters
    filters = [
        # Retweets
        lambda t: True if re.search(r'\bRT\b', t) is None else False
        # Empty
        ,lambda t: t.strip() != ''
        # Mad Hashtaggers
        ,lambda t: t.count('#') < 4
        # Dropping tweets with filthy things such as usernames
        ,lambda t: True if re.search(r'\b\w[0-9_]+\w*\b', t) is None else False
    ]

    # Tweet Cleaners
    cleaners = [
        # Dropping special characters
        lambda t: re.sub(re.compile('[^'+string.printable+']'), '', t)
        # Dropping urls, hashtags and addressing
        ,lambda t: re.sub(r'\bhttps?://.*\b', '', t)
        # Dropping hashtags and addressing
        ,lambda t: re.sub(r'#|@[^ ]?|\*', '', t)
        # Dropping htmlentities
        ,lambda t: re.sub(r'&.+?;', '', t)
        # Final Strip
        ,lambda t: t.rstrip().strip()
    ]

    # Constructor
    #------------
    def __init__(self, kigo):
        self.syl = SylModule(self.settings.sonorities)
        self.kigo = kigo

        # Initializing sentence tokenizer
        self.sentence_detector = nltk.data.load(self.settings.pickle)

        # Initializing haiku
        self.haiku = Haiku(self.kigo)

    def procede(self, tweets):

        # Reinitializing haiku
        if self.haiku.isComplete():
            self.haiku.reinit(self.kigo)

        # Launching Protocol Loop
        for tweet in tweets:

            # Filtering and Cleansing
            if self.filterTweet(tweet):
                tweet = self.cleanTweet(tweet)

                # Tokenization
                tokens = self.sentence_detector.tokenize(tweet)
                if self.isHaikuMaterial(tokens):
                    return True
        return False

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
        
        # Looping through sentences
        for sentence in tokens:
            for semi_sentence in sentence.split(','):
                
                # Counter Init
                counter = 0

                # To words and counting syllables
                semi_sentence = re.sub(self.punctuation_re, '', semi_sentence)
                words = nltk.word_tokenize(semi_sentence)
                
                # Counting Syllables
                for word in words:
                    counter += self.countSyllables(word)

                # Keeping Relevant parts
                if counter >= 4 and counter < 6:
                    self.haiku.setShortVerse(semi_sentence)
                else:
                    if counter >= 6 and counter  <= 8:
                        self.haiku.setLongVerse(semi_sentence)

                if self.haiku.isComplete():
                    return True
        return False

    # Helpers
    #---------
    def countSyllables(self, word, dict=None):
        return len(self.syl.syllabify(word).split('.'))



