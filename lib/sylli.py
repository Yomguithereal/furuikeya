#!/usr/bin/python
#----------------------------------------------------------------------------
# Name:         sylli.py
# Purpose:      Syllable and syllabification.
#
# Author:       Iacoponi Luca
#
# Created:      June 2009
# Licence:      Apache Licence
#----------------------------------------------------------------------------

# FIX:
# * Read files

# DO:
# * pak:o > pakko
# * sonority distance
# * demo should be costum
# * syllabify orthographic
# * i18n?
# * check integration with nltk
# * Syllable generator

""" Syllable and syllabification Tool """

import sys
import re
import os
import shutil
import ConfigParser


class PhSegment:
    """ This class defines a phonological segment.

    >>> segment = PhSegment(['p', '1', 'O'])

    It is made of the segmental phonological representation

    >>> print segment.segment
    p

    The sonority of the segment

    >>> print segment.son
    1

    The natural class (O=Occlusives, F=Fricatives, V=Vowel etc.)

    >>> print segment.pclass
    O

    The CV node, which defines whether the segment is
    (C)onsonat or vowel (V)

    >>> print segment.cvcv
    C
    """

    def __init__(self, properties):
        try:
            self.segment = properties[0].strip()
            self.son = int(properties[1].strip())
            self.pclass = properties[2].strip()
        except IndexError:
            print("Sonority Error: Ill-formed sonority value.\n" + \
            'Remember a value should consist of three comma-separated ' + \
            "values. For example\na = a, 22, V")
            sys.exit(1)
        if self.pclass == 'V':
            self.cvcv = 'V'
        else:
            self.cvcv = 'C'


class SylModule:
    """ Core syllabification module. """
    def __init__(self, sonority):
        """ Class initialisation. A lexicon, which is a ConfigParser object
        is required.

        >>> syl = SylModule()

        self.output define the output form. It defines which attribute of the
        PhSegment object as to be printed. This can be the segment

        >>> syl.output = 'str'
        >>> print syl.syllabify('kasa')
        ka.sa

        The natural class

        >>> syl.output = 'cvg'
        >>> print syl.syllabify('kasa')
        OV.FV

        Or the cvcv structure

        >>> syl.output = 'cvcv'
        >>> print syl.syllabify('kasa')
        CV.CV

        self.boundaries will containes the index of syllable boundaries
        after the SA had been run

        >>> bb = syl.syllabify('kasetta')
        >>> print syl.boundaries
        [2, 5]
        """

        # Attributes defined in self.load_conf()
        self.boundaries = []
        self.verbose = 0
        self.sonority_file = ''
        self.lexicon = ''
        self.output = ''
        self.extra = 0

        # Read and load the config file
        self.load_conf(sonority)

    def load_conf(self, sonority_file):
        """Load $HOME configuration file sonority.txt.
        It first looks if $HOME/.sylli is already there, if not it creates it.
        It then set the attribute self.sonority_file (sonority filename)
        and self.lexicon (ConfigParser object).

        >>> syl = SylModule()
        >>> syl.load_conf('config/sonority.txt')
        True

        The class method also sets most class attributes

        >>> print syl.output, syl.extra
        str 1
        """
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        try:
            config.read(sonority_file)
        except Exception as err:
            print("File contains parsing errors: " + sonority_file)
            print(err)
            return False

        self.sonority_file = sonority_file
        self.lexicon = config
        self.output = self.fetch_lexicon('output', section='General')
        self.extra = int(self.fetch_lexicon('extra', section='General'))

        return True

    def syllabify(self, sequence):
        """ It goes through the three sub-modules/methods of the class.
        First it transduce the sequence, then it ships it to the SA and
        finally to the output transducer. The main method of the class.

        >>> syl = SylModule()
        >>> syl.syllabify('kasa')
        'ka.sa'
        """
        ph_sequence = self.input_transducer(sequence)
        syllabified = self.sa(ph_sequence)
        return self.output_transducer(syllabified)

    def input_transducer(self, input_string, transducer=0):
        """ The transducer can perform only two operations: Ship and Translate.
        Translate converts a string into the corresponding phonological object
        Ship, ships a translated sequence to the Syllabification Algorithm.

        >>> syl = SylModule()
        >>> for seg in syl.input_transducer('io'):
        ...     print seg.segment, seg.son, seg.pclass
        i 22 V
        o 22 V
        """
        # A list of phonological converted objects
        ph_sequence = []
        # remove whitespaces
        input_string = re.sub(r"\s+", "", input_string)
        # Manage different tranducers
        if transducer:
            return False

        # For each segment either translate or ship to the SA
        for input_segment in input_string:
            # Translate
            phson = self.fetch_lexicon(input_segment)
            # Symbols to ignore have sonority = 0 or are not specified in the
            # lexicon
            if not phson:
                continue
            ph_segment = PhSegment(phson.split(','))
            # Ship
            if ph_segment.son == 99:
                ph_sequence.append(ph_segment)
                self.sa(ph_sequence)
                ph_sequence = []
            # Translate and move on
            else:
                ph_sequence.append(ph_segment)
        # All input translated, ship
        return ph_sequence

    def sa(self, sequence):
        """ Divide a phonematic sequence into syllables.
        The sequence is list of phonological objects. Each object is
        evaluated using an extremely simple syllabification algorithm
        based on the Sonority Sequencing Principle. It puts a syllable
        boundary after every minimum,
        or when two consequtive sonorities are equal

        >>> syl = SylModule()
        >>> ph_sequence = syl.input_transducer('io')
        >>> for seg in syl.sa(ph_sequence):
        ...     print seg.segment, seg.son, seg.pclass
        i 22 V
        o 22 V
        """
        # We add a final segment to avoid the algorithm to overshoot
        boundaries = []
        null_segment = PhSegment(['0', '0', '0'])
        sequence.append(null_segment)
        len_sequence = len(sequence)
        # SSA
        # find least sonorous segments
        for i in range(1, len_sequence - 1):
            if (sequence[i-1].son > sequence[i].son  and \
            sequence[i+1].son > sequence[i].son) or \
            sequence[i-1].son == sequence[i].son:
                boundaries.append(i)
        self.boundaries = boundaries
        # remove the final null segment
        sequence = sequence[:-1]
        return sequence

    def output_transducer(self, sequence):
        """ Segments, sonorities, natural classes and
        syllable boundaries are flattened into one dimension ready to be
        printed in a sequential, phisical form.

        >>> syl = SylModule()
        >>> psequence = syl.input_transducer('kasa')
        >>> syllabified = syl.sa(psequence)
        >>> syl.output_transducer(syllabified)
        'ka.sa'
        """
        syllabified = ''
        # create a string from the object t
        for seg in sequence:
            if self.output == 'str':
                item = seg.segment
            elif self.output == 'cvg':
                item = seg.pclass
            elif self.output == 'cvcv':
                item = seg.cvcv
            syllabified += item

        len_sequence = len(syllabified)
        # Add the syllable boundaries
        for boundary in self.boundaries:
            bound_position = boundary - len_sequence
            syllabified = syllabified[0:bound_position] + \
                          '.' + syllabified[bound_position:]

        # Include extrasyllabic segments in the following syllable if necessary
        if not self.extra:
            vowel = 0
            i = 0
            for segment in syllabified:
                # syllable boundary preceeded by no vowel (or sonorants)
                if segment == '.':
                    if not vowel:
                        syllabified = syllabified[0:i] + syllabified[i+1:]
                    vowel = 0
                # Get the segment class and check if it's a vowel
                else:
                    curr_seg = PhSegment(self.fetch_lexicon(segment).split(','))
                    if curr_seg.pclass == 'V': # or a.class != 'S'
                        vowel = 1
                i += 1

        return syllabified

    def fetch_lexicon(self, option, section="Segments"):
        """ Return a phonological segment or an option from the sonority file.
        The sonority file to be used is specified in self.lexicon.

        >>> syl = SylModule()
        >>> syl.fetch_lexicon('a')
        'a, 22, V'
        >>> syl.fetch_lexicon('output', section='General')
        'str'
        """
        try:
            value = self.lexicon.get(section, option)
            if value != None:
                return value
            else:
                if self.verbose:
                    print("E: Sonority file contains errors!\n")
                return False
        except Exception as err:
            if self.verbose:
                print("E: Sonority file contains errors!\n", err)
            return False