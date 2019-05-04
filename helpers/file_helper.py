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
import sys
import pandas
import json
from pathlib import Path

from helpers.multi_helper import console_data_printer

'''
    This helper includes the methods:.

'''


def excel_parser(path):
    """
    This function reads an excel file which contains the original data set as provided.
    :param path:
    :return songs_from_data_set:
    """
    # todo wtf=======================
    xls = pandas.ExcelFile(path)
    df = xls.parse(xls.sheet_names[0])
    bf = df.to_dict()
    # ================================

    songs_from_data_set = dict()

    for i in range(len(bf['tittle'])):
        songs_id = "song_" + "{0:0=4d}".format(i)
        songs_from_data_set[songs_id] = {'tittle': bf['tittle'][i],
                                         'artist': bf['artist'][i],
                                         'composer': bf['composer'][i],
                                         'year': bf['year'][i],
                                         'lyrics': [bf['lyrics'][i]]}

    return songs_from_data_set


def file_cleaner(type_of_call="saving_progress"):
    """
    This function cleans the files apostrophe_cases, grouped_results, songCompDict and song_data_set by default.
    If the user has proceeded and they exist, change_log and change_log_double_words are cleaned as well.
    :param type_of_call:
    :return:
    """
    if not os.path.exists(os.path.join(Path(os.getcwd()).parent, "result_files")):
        os.makedirs(os.path.join(Path(os.getcwd()).parent, "result_files"))

    open(os.path.join(Path(os.getcwd()).parent, "result_files", "apostrophe_cases.json"), 'w', encoding='utf-8')
    open(os.path.join(Path(os.getcwd()).parent, "result_files", "grouped_results.json"), 'w', encoding='utf-8')
    open(os.path.join(Path(os.getcwd()).parent, "result_files", "song_data_set.json"), 'w', encoding='utf-8')
    if type_of_call != "saving_progress":
        open(os.path.join(Path(os.getcwd()).parent, "result_files", "change_log.json"), 'w', encoding='utf-8')
        open(os.path.join(Path(os.getcwd()).parent, "result_files", "change_log_double_words.json"), 'w', encoding='utf-8')


def json_reader(name):
    """
    This function is used to read other files, specifically those generated after the apostrophe cases
    have been found.
    :param name:
    :return data (as dict):
    """
    file_dir_name = os.path.join(Path(os.getcwd()).parent, "result_files", name + '.json')
    with open(file_dir_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return dict(data)


def json_writer(something_to_write, name):
    """
    writes the results in a file
    :param something_to_write:
    :param name:
    :return:
    """
    file_dir_name = os.path.join(Path(os.getcwd()).parent, "result_files", name + '.json')
    with open(file_dir_name, 'w', encoding='utf-8') as outfile:
        json.dump(something_to_write, outfile, ensure_ascii=False, indent=4)


def check_datasets():
    path = os.path.join(Path(os.getcwd()).parent, "data")
    try:
        data_contents = []
        data_contents = os.listdir(path)
        return data_contents
    except FileNotFoundError:
        print("Directory ", Path(os.getcwd()).parent + "\data", "does not exist! Abort.")
        exit(1)


def choose_dataset():
    datasets = check_datasets()
    console_data_printer("Available datasets:", datasets)
    checker = False
    while not checker:
        try:
            chosen_dataset = int(input("Choose among the available datasets: "))

            while 0 <= chosen_dataset < len(datasets):
                checker = True
                break
            else:
                raise ValueError("Please choose from 0 to {}".format(len(datasets)-1))

        except ValueError as e:
            print("The input you gave is not acceptable... Try again.\nError message: ", str(e), "\n")

    path_to_songs = os.path.join(os.path.join(Path(os.getcwd()).parent, "data"), datasets[chosen_dataset])
    return path_to_songs
