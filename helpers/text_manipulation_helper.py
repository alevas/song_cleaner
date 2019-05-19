"""
Copyright (c) 2019 Alexandros Vasileiou

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re

'''
    This helper includes all the methods that help with manipulating text. 
    mark_repetition
    punctuation_clean_up
'''


def mark_repetitions(lyric):
    """
        This function marks the repetition start and finish
        :param lyric: the whole lyric as a string
        :return lyric (after marking the repetition):
    """
    # todo improve the regex's. simplify and cover other cases of repetitions.
    # todo include cases were the repetitions were written with greek letter 'χ'

    standard_rep_start = "["
    standard_rep_end = "] x2"
    found_rep_patterns = ["\){1}\s{0,}\({0,}[x]{0,}\s{0,}\d{1}[x]{0,}\s{0,}\){0,}",
                          "\}{1}\s{0,}\({0,}[x]{0,}\s{0,}\d{1}[x]{0,}\s{0,}\){0,}",
                          "\}{1}\s{0,}\({0,}[χ]{0,}\s{0,}\d{1}[χ]{0,}\s{0,}\){0,}",
                          "\]{1}\s{0,}\({0,}[χ]{0,}\s{0,}\d{1}[χ]{0,}\s{0,}\){0,}",
                          "\){1}\s{0,}\({0,}δις\s{0,}\){0,}"]
    for i in found_rep_patterns:
        if re.findall(i, lyric, re.IGNORECASE):
            lyric = lyric.replace('[', standard_rep_start)
            lyric = lyric.replace('{', standard_rep_start)
            lyric = lyric.replace('(', standard_rep_start)
            lyric = re.sub(i, standard_rep_end, lyric)

    return lyric


def punctuation_clean_up(lyric):
    """
    Makes a punctuation marks cleanup.

    :param lyric: the whole lyric as a string
    :return lyric (without current puncuation marks:
    """

    general_apostrophe = '’'
    punctuation_mark_replacement = ''

    # Add whatever is to be removed to the following list.
    punctuation_marks_to_go = [',',
                               '.',
                               ';',
                               '!',
                               ':',
                               '«',
                               '»',
                               '?',
                               '-',
                               '|',
                               '\\',
                               '/',
                               '\"',
                               ')',
                               '('
                               '{',
                               '}']  # NOTE: Remove the parenthesis if repetitions have been marked already.
    # Sometimes a slightly different version of an apostrophe symbol is used. In the same fashion as above.
    apostrophes_to_go = ['΄',
                         '\'']

    for i in punctuation_marks_to_go:
        lyric = lyric.replace(i[0], punctuation_mark_replacement)
    for i in apostrophes_to_go:
        lyric = lyric.replace(i[0], general_apostrophe)

    return lyric
