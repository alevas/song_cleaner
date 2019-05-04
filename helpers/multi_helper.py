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
import itertools
import operator
import re
import sys

from copy import deepcopy

from tabulate import tabulate

"""
    This is a script of various helpers. Methods are:
    console_data_printer
    cross_check_apostrophe_total
    group_apostrophes
    query_yes_no
    tokenize_on_token
    
"""


def console_data_printer(message=None, data=None, data_headers=None):
    """
        Prints info with separators above and bellow or tabulated if the data exist.
        :param message:
        :param data:
        :param data_headers:
        :return:
    """
    if message is not None:
        print('=' * 100)
        print(message.center(100, "*"))
        print('=' * 100 + '\n')
    if data is not None and data_headers is not None:
        if isinstance(data, list):
            print(tabulate(data, headers=data_headers))
        else:
            print(tabulate((data[x] for x in data), headers=data_headers, tablefmt="fancy_grid"))
        print('=' * 100 + '\n')
    elif data is not None:
        if isinstance(data, list):
            print("yayayayaya")
            print(tabulate([data], headers=[x for x, i in enumerate(data)], tablefmt="fancy_grid"))


def cross_check_apostrophe_total(line):
    """
        Double checks if we found the correct number of apostrophes using
        a simple regular expression on the basic material
        :param line:
        :return counter:
    """
    counter = 0
    if len(line) > 0:
        if isinstance(line, list):
            temp_string = ""
            for i in line:
                temp_string += i
                temp_string += " "
            line = temp_string
        if re.findall("\w*΄\w*|\w*’\w*|\w*'\w*", line):
            counter = len(re.findall("\w*΄\w*|\w*’\w*|\w*'\w*", line))
    return counter


def group_apostrophes(ungrouped_apostrophe_cases):
    """
        This function groups apostrophe cases into apostrophe groups. E.g. if three occurenses of an apostrophe case
        are found, this function will create a dictionary entry in the return dict that contains the word, the apostrophe
        case id's and the word's frequency.
        :param ungrouped_apostrophe_cases:
        :return: grouped_results:
    """
    # todo pack this up a bit (most common)
    # get an iterable of (item, iterable) pairs
    sorted_upc = sorted((ungrouped_apostrophe_cases[x]['apostr_word'], x) for x in ungrouped_apostrophe_cases)
    groups = itertools.groupby(sorted_upc, key=operator.itemgetter(0))
    grouped_results_list = []

    # auxiliary function to get "quality" for an item

    def _auxfun(g):
        item, iterable = g
        count = 0
        indexes = []
        for _, where in iterable:
            count += 1
            indexes.append(where)
        grouped_results_list.append({'apostr_case': item,
                                     'frequency': count,
                                     'apostr_cases_ids': indexes})
        return count, indexes

    print("The group with the highest frequency is: ", max(groups, key=_auxfun)[0])

    grouped_results = {}
    for key, i in enumerate(grouped_results_list):
        group_id = "group_" + "{0:0=4d}".format(key)
        grouped_results[group_id] = deepcopy(i)

    return grouped_results


def query_yes_no(question, default=None):  # ok
    """
        Ask a yes/no question via input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "υ": True, "υεσ": True, "υε": True, "υες": True,
             "no": False, "n": False, "νο": False, "ν": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower().strip()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def tokenize_on_token(to_tokenize, pattern, token):
    """
        Tokenizes a string based on a given pattern and desired token.
        :param to_tokenize:
        :param pattern:
        :param token:
        :return to_tokenize (now tokenized):
    """
    if re.search(pattern, to_tokenize):
        to_tokenize = re.sub(pattern, token, to_tokenize)
    return to_tokenize
