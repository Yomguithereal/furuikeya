#!/usr/bin/env python
#
# Author: jacoponi@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#

""" Syllabification demo """

import sylli

def main():
    """ Run the demo """
    syl = sylli.SylModule()
    demo(syl)

def demo(syl, phn=0):
    """ A demo showing most relevant syllabifications in Italian

    >>> syl = sylli.SylModule()
    >>> demo(syl) # doctest:+ELLIPSIS
    <BLANKLINE>
    Frequent clusters:
    pane -> pa.ne
    OLLo -> OL.Lo
    ...
    """

    print("\nFrequent clusters:")
    for wrd in ['pane', 'OLLo', 'aja', 'per', 'batSo']:
        print(wrd + ' -> ' + syl.syllabify(wrd))

    print('\nCL clusters (pl, kr, dr etc.):')
    for wrd in ['padre', 'litro', 'kapra']:
        print(wrd + ' -> ' + syl.syllabify(wrd))

    if phn:
        print('\nsC clusters (PHN, s -> z):')
        for wrd in ['pasta', 'strano', 'nikilizmo',
                    'zdentato', 'izraele', 'perstrada']:
            print(wrd + ' -> ' + syl.syllabify(wrd))

    else:
        print('\nsC clusters (STD):')
        for wrd in ['pasta', 'strano', 'nikilismo', 'sdentato',
                    'israele', 'perstrada']:
            print(wrd + ' -> ' + syl.syllabify(wrd))

    print('\nAffricates:')
    for wrd in ['tsio', 'pattso', 'roddzo', 'dzOrro', 'dZorno', 'paddZo',
                'tSao', 'batSo', 'kseno', 'ekstra']:
        print(wrd + ' -> ' + syl.syllabify(wrd))

    print('\nGeminates:')
    print('gatto -> ' + syl.syllabify('gatto'))
    print('gallo -> ' + syl.syllabify('gallo'))

    print('\nVowel clusters:')
    for wrd in ['paura', 'dzia', 'paolo', 'koala', 'pjano', 'ajwOla', 'Oboe']:
        print(wrd + ' -> ' + syl.syllabify(wrd))

    print('\nOther clusters:')
    for wrd in ['ipnOzi', 'sinaptiko', 'nafta',
                'atletiko', 'abnorme', 'kapsula']:
        print(wrd + ' -> ' + syl.syllabify(wrd))

if __name__ == "__main__":
    main()
