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
import getopt
import configparser
import filepath
import demo

VERSION = '0.9.8'

def main(argv):
    """ Run the command line script.

    Note that Sylli always requires an argument.

    >>> main(argv='') #doctest: +ELLIPSIS
    sylli: use at least one argument...

    The simplest way to use Sylli is to syllabify a string

    >>> main(['-s', 'la kapra'])
    la.ka.pra

    You can also syllabify a timit file, which will be parsed as single string.

    >>> main(['-f', 'test/files/sample.phn'])
    no.na.i.u.na.farf.fal.la.al.lo.ra.swo.pra.la.mi.a.mak.kji.ni.nab.blu

    Or a text file. The lines are feeded into sylli one by one.

    >>> main(['-f', 'test/files/sample.txt'])
    O.vis.to.u.na.vol.pe.ne.ra
    trop.pes.tel.le.bril.la.no.in.tSE.lo

    or a directory:

    >>> main(['-d', 'test/files'])
    ma.i.o.nO.tSe.lO.la.far.fal.la
    O.vis.to.u.na.vol.pe.ne.ra.trop.pes.tel.le.bril.la.no.in.tSE.lo
    no.na.i.u.na.farf.fal.la.al.lo.ra.swo.pra.la.mi.a.mak.kji.ni.nab.blu

    You can also run a demo of the program

    >>> main(['-z']) #doctest: +ELLIPSIS
    <BLANKLINE>
    Frequent clusters:
    pane -> pa.ne
    OLLo -> OL.Lo
    ...

    Other options allow you to print the current version

    >>> main(['-v']) #doctest: +ELLIPSIS
    sylli-0.9.8
    Copyright 2010 Luca Iacoponi...

    Or the help screen

    >>> main(['-h']) #doctest: +ELLIPSIS
    Usage: sylli [OPTION]... [FILE|string]...

    Sylli will automatically look for the sonority.txt in your $HOME.
    But you can always use another configuration file.
    Remember to use -c option before any other.

    >>> main(['-c', 'test/crazysonority.txt', '-s', 'papa'])
    p.a.p.a

    Finally, you can run sylli in interactive mode.

    >>> main(['-i']) #doctest: +SKIP
    """

    try:
        opts, args = getopt.getopt(argv, "hf:zd:s:c:vi", ["help", "file=", \
                     "demo", "directory=", "string=", "version", \
                     "config=", "interactive",])

    except getopt.GetoptError as err:
        print("sylli: " + str(err))
        print("Try `sylli --help' for more information.")
        return 2

    syl = SylModule()
    if not opts:
        print("sylli: use at least one argument.")
        print("Try `sylli --help' for more information.")
        return 2

    for opt, arg in opts:
        # print opt
        if opt in ("-h", "--help"):
            print(usage())
            return 0

        if opt in ("-c", "--config"):
            syl.load_conf(arg)

        elif opt in ('-z', "--demo"):
            demo.demo(syl)

        elif opt in ("-f", "--file"):
            to_syll = filel(arg)
            if not to_syll:
                print("Sorry, file does not exists: " + arg)
                return 0
            else:
                for line in to_syll:
                    print(syl.syllabify(line))

        elif opt in ("-d", "--dir"):
            file_list = dirl(arg)
            # syllabify each file
            for key in file_list:
                if file_list[key]:
                    print(syl.syllabify(' '.join(file_list[key])))

        elif opt in ("-s", "--string"):
            print(syl.syllabify(arg))

        elif opt in ("-v", "--version"):
            print(version())

        elif opt in ("-i", "--interactive"):
            while 1:
                try:
                    sinput = input('--> ')
                    print(syl.syllabify(sinput))
                except KeyboardInterrupt:
                    return 0

def usage():
    """ Return usage help.

    >>> print usage() #doctest: +ELLIPSIS
    Usage: sylli [OPTION]... [FILE|string]...
    Divides a file, a string or a directory into syllable....
    """

    usage_str = """Usage: sylli [OPTION]... [FILE|string]...
Divides a file, a string or a directory into syllable.

  -d, --directory            syllabify the content of a directory.
  -r, --recursive            syllabify directory recursively.
  -f, --file                 syllabify the content of a file.
  -s, --string               syllabify a string.
  -c, --config               force the use of an alternative sonority file.
                             It should always be used as the first argument.
  -z, --demo                 show a list of syllabifications examples.
  -h, --help                 display this help and exit.
  -v, --version              output version information and exit.

Exit status is 0 if OK, 1 if minor problem, 2 if serious trouble.
Time markers in timit files are automatically stripped off.

Example: sylli -s "la kapra"

Report bugs to <jacoponi@gmail.com>."""
    return usage_str

def version():
    """ Return the version of the program and other information

    >>> print version() #doctest: +ELLIPSIS
    sylli-0.9.8
    Copyright 2010 Luca Iacoponi...
"""

    vers =  'sylli-' + VERSION + "\n"
    vers += """Copyright 2010 Luca Iacoponi

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
    return vers

def dirl(input_dir, ext=0):
    """ Return a dictionary of the form filename:content of a directory

    >>> dirl('test/files/') #doctest: +ELLIPSIS
    {'test/files/sample.std': ['__ ma% %"io nO tSe l-"O la farf"alla']...

    You can specify a file extention, in this case, only files with such
    extension will be parsed.

    >>> print dirl('test/files/', ext='std')
    {'test/files/sample.std': ['__ ma% %"io nO tSe l-"O la farf"alla']}
    """

    # input_dir = os.path.normpath(input_dir)
    # Check if directory exists
    if not os.path.isdir(input_dir):
        return False

    file_dict = {}
    # process files matching extension
    for input_f in os.listdir(input_dir):
        if ext == input_f[-3:] or not ext:
            absfile = os.path.join(input_dir, input_f)
            # create a dictionary of the form filename:content
            file_dict[absfile] = filel(absfile)

    return file_dict

def filel(input_f):
    """ Return a a list of string with the content of a file, if it is a TIMIT,
    it stript the TIMIT off.

    >>> filel('test/files/sample.std')
    ['__ ma% %"io nO tSe l-"O la farf"alla']
    """

    # input_f = os.path.normpath(input_f)
    if not os.path.isfile(input_f):
        return False

    converted = detimit(input_f)

    # It is a TIMIT
    if converted:
        converted = [' '.join(converted)]

    # it is not a TIMIT, each line is returned as an element of a list
    if not converted:
        converted = []
        to_convert = open(input_f, 'r')
        for line in to_convert:
            converted.append(line)

    # Good text file
    if converted:
        return converted

def detimit(timitf):
    """ strip out TIMIT off a file.

    >>> detimit('test/files/sample.std')
    ['__', 'ma%', '%"io', 'nO', 'tSe', 'l-"O', 'la', 'farf"alla']
    """

    # timitf = os.path.normpath(timitf)
    new_list = []
    timit = open(timitf, 'r')
    for line in timit:
        if len(line.split()) != 3:
            return False
        else:
            new_list.append(line.split()[-1])
    return new_list

def reset_son():
    """ Restore installation sonority overwriting current sonority"""
    inst = filepath.get_path('inst_sonority')
    usr = filepath.get_path('usr_sonority')
    try:
        shutil.copyfile(inst, usr)
        print(usr + " created.")
    except Exception as err:
        print('(E) Could not copy sonority.txt: ' + inst + ' -> ' + usr)
        print(err)
        return False
    return True


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
    def __init__(self, sonority = filepath.get_path('usr_sonority')):
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

        # No home directory for sylli found, create it
        config_dir = filepath.get_path('config_dir')
        if not os.path.exists(config_dir):
            print('No user directory found, creating: ' + config_dir)
            os.mkdir(config_dir, 0o700)
            shutil.copyfile(filepath.get_path('inst_sonority'),
                            filepath.get_path('usr_sonority'))

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
        config = configparser.ConfigParser()
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
        input_string = re.sub("\s+", "", input_string)
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

if __name__ == "__main__":
    main(sys.argv[1:])
