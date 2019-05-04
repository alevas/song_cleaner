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
import os
import re
from copy import deepcopy
import nltk

from helpers import file_helper, multi_helper, text_manipulation_helper
from helpers.file_helper import json_writer
from helpers.multi_helper import console_data_printer


def apostrophe_finder(path_to_songs):
    """
        Reads an excel file with songs. Performs tokenization upon it.

    :param path_to_songs:
    :return apostrophe_cases, grouped_results, song_data_set:
    """
    print("Initiate apostrophe_finder. Wait until the data set is under examination...")
    song_data_set = deepcopy(file_helper.excel_parser(path_to_songs))

    # we have to do this to ensure that the files we wish to write to do not keep junk from other runs.
    file_helper.file_cleaner("restart")

    # pattern for finding greek apostrophes
    pattern_apostrophe = "(\’\w*)|(\w*\’)|(\w*\’\w*)"

    # patterns for lyrics, verses, repetition start & finish
    patterns = {"lyric": '\n',
                "verse": '\n\n',
                "rep_begin": '\[',
                "rep_end": '\s*\]\s*x\d', }

    # tokens for lyrics, verses, repetition start & finish
    tokens = {"lyric": ' LYRIC ',
              "verse": ' VERSE ',
              "rep_begin": ' REPSTART ',
              "rep_end": ' REPFIN '}

    # count number of apostrophes
    apostrophes_counter = 0
    apostrophes_total = 0
    apostrophe_cases = dict()
    apostr_id = 0

    for songId in song_data_set:
        if len(song_data_set[songId]['lyrics']) > 0:
            line = ''.join(song_data_set[songId]['lyrics'])

            # will be used in the end to check if we found all the apostrophes using a simple regular ex.
            apostrophes_total += multi_helper.cross_check_apostrophe_total(line)

            # here we remove any punctuation marks and tries to convert stuff to be under unified patterns
            line = text_manipulation_helper.mark_repetitions(line)
            line = text_manipulation_helper.punctuation_clean_up(line)

            # mark verses, lyrics, repetitions
            for i in sorted(patterns.keys()):  # the sorted ensures this order: lyric, verse, rep_begin, rep_end
                line = multi_helper.tokenize_on_token(line, patterns[i], tokens[i])

            # the next line does not work for greek. OK with latin letters, though
            # line = nltk.word_tokenize(line)
            line = nltk.WhitespaceTokenizer().tokenize(line)

            # search each tokenized song per word
            for word_index, j in enumerate(line):
                if re.findall(pattern_apostrophe, j):
                    apostrophes_counter += len(re.findall(pattern_apostrophe, j))

                    # in this dictionary we insert the context values we wish to write to file, after we check
                    # if those values exist
                    temp_dict = {}

                    for i in [-2, -1, 1, 2]:
                        if 0 <= word_index + i < len(line):
                            temp_dict[word_index + i] = line[word_index + i]
                        else:
                            temp_dict[word_index + i] = ""

                    apostrophe_id = "apostrophe_" + "{0:0=4d}".format(apostr_id)
                    apostrophe_cases[apostrophe_id] = {'apostr_word': j.lower(),
                                                       'song_id': songId,
                                                       'position': word_index,
                                                       'word-2': temp_dict[word_index - 2].lower(),
                                                       'word-1': temp_dict[word_index - 1].lower(),
                                                       'word+1': temp_dict[word_index + 1].lower(),
                                                       'word+2': temp_dict[word_index + 2].lower()}
                    apostr_id += 1
            song_data_set[songId]['lyrics'] = line

    # here we find the most common apostrophe cases and write them to a file called grouped_results.json
    grouped_results = multi_helper.group_apostrophes(apostrophe_cases)

    # write the apostrophe cases, groups & the whole data set to json files

    for i, j in zip([apostrophe_cases, grouped_results, song_data_set],
                    ['apostrophe_cases', 'grouped_results', 'song_data_set']):
        json_writer(i, j)

    # check if we actually found all the apostrophes the initial data set has
    if apostrophes_counter == apostrophes_total:
        print("Found", apostrophes_counter, "cases of apostrophes. Good luck!")
    else:
        raise Exception("Some apostrophes appear to be missing. Check your code again!")

    return apostrophe_cases, grouped_results, song_data_set


if __name__ == "__main__":
    console_data_printer("Apostrophe_Break on standalone mode.")
    apostrophe_finder(os.getcwd() + "\\data" + "\\stixoi.xlsx")
