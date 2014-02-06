# -------------------------------------------------------------------
# Haiku Abstraction
# -------------------------------------------------------------------
#
#
#   Author : PLIQUE Guillaume
#   Version : 1.0

# Dependencies
#=============
import re
import random

# Main Class
#=============
class Haiku:
    ''' The Haiku class is just a mere abstraction of what
    furuikeya will be able to output. It handles its verses,
    its kigo and its kireji'''

    # Properties
    kigo = None
    kigo_in_verses = False
    kireji_position = None
    kireji = None
    kireji_list = [';', ',', ' -']
    verses = ['', '', '']
    string = ''

    uppercase_re = r'[A-Z]{2,}'
    weirdspace_re = r' {2,}'

    # Constructor
    def __init__(self, kigo) :

        # Kireji Position
        #   0 = between first and second verse
        #   1 = between second and third verse
        self.kireji_position = random.randint(0, 1)

        # Possible kireji
        self.kireji = random.choice(self.kireji_list)

        # Kigo
        self.kigo = kigo

    # Reinitialization
    def reinit(self, kigo):
        self.__init__(kigo)
        self.verses = ['', '', '']
        self.kigo_in_verses = False
        self.string = ''

    # Printing
    def __repr__(self):
        if self.isComplete():
            return self.output()
        else:
            return 'Haiku is not complete'

    # Setters
    def _checkKigoInVerse(self, verse):
        if verse.lower().count(self.kigo) > 0:
            self.kigo_in_verses = True
        return self.kigo_in_verses

    def _lastVerse(self):
        return len([i for i in self.verses if i == '']) == 1

    def _strip(self, verse):

        # CAPS LOCK fools
        if re.search(self.uppercase_re, verse) is not None:
            verse = verse.lower()

        # Weird spacing correction
        verse = re.sub(self.weirdspace_re, ' ', verse)

        # Basic stripping
        return verse.strip().rstrip()

    def setLongVerse(self, verse):
        
        # Verification
        if self.verses[1] != '':
            return False
        if not self._checkKigoInVerse(verse) and self._lastVerse():
            return False
        
        # Setting
        self.verses[1] = self._strip(verse)


    def setShortVerse(self, verse):

        # Verifications
        if self.shortVersesComplete():
            return False
        if not self._checkKigoInVerse(verse) and self._lastVerse():
            return False

        # Setting
        if self.verses[0] == '':
            self.verses[0] = self._strip(verse)
        else:
            self.verses[2] = self._strip(verse)


    # Output method
    def output(self) :
        if self.string.strip() == '':
            for nb, verse in enumerate(self.verses):
                self.string += '\t'+verse
                if nb == self.kireji_position:
                    self.string += self.kireji
                if nb < 2:
                    self.string += '\n'
        return self.string

    # Completion
    def isComplete(self):
        return len([i for i in self.verses if i == '']) == 0

    def shortVersesComplete(self):
        return len([i for i in [self.verses[0], self.verses[2]] if i == '']) == 0
