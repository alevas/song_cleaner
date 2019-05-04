#!/usr/bin/env python3

"""
Copyright (c) 2017 Alexandros Vasileiou

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
from json import JSONDecodeError

from song_cleaner.Apostrophe_Break import apostrophe_finder
from song_cleaner.Apostrophe_Eliminator import apostrophe_killer
from helpers.file_helper import json_reader, choose_dataset
from helpers.multi_helper import query_yes_no, console_data_printer


'''
    steps
    A. ask if the user wishes to start all over.
        1. ask again to make sure.
            a. If yes:
                i. read the /data directory and ask for which data set to use.
                ii.  invoke the apostrophe breaker to tokenize the data set and go to step B.
            b. if no:
                go back to ask if the user wishes to start all over.
        2. if not, read the files apostrophe_cases, group_results & songsCompDict in the directory result_files 
    B. ask if the apostrophe_eliminator should be invoked.   
    
    ! An exception is thrown in case either the data set or the result files are missing.
        
    !!! IMPORTANT NOTICE TO USER!!!
    Since there is a certain issue when reading files opened previously by excel, please check the written 
    song_data_set.txt for any encoding errors. It usually looks like this: "\\\\\x91". Be extra careful not to cause 
    changes to the order of the song's apostrophe marked words, which would cause extreme problems when trying to 
    replace them.     
'''


def song_cleaner():  # ok

    console_data_printer("This is the Song_Cleaner_Project! It cleans songs.")

    try:

        while query_yes_no("Do you wish to start afresh?"):

            if query_yes_no("WARNING: This will delete all previous progress. Are you sure? "):
                path_to_songs = choose_dataset()
                apostrophe_cases, grouped_results, song_data_set = apostrophe_finder(path_to_songs)

                break

            else:
                print("Please, choose again.")

        else:

            apostrophe_cases = json_reader("apostrophe_cases")
            grouped_results = json_reader("grouped_results")
            song_data_set = json_reader("song_data_set")

        # this step is performed as the change_log and change_log_double_words files are not generated by default
        # by the apostrophe_finder, so the .json files may have never been created.
        try:
            change_log = json_reader("change_log")
            change_log_double_words = json_reader("change_log_double_words")
        except JSONDecodeError:
            change_log = dict()
            change_log_double_words = dict()

        if query_yes_no("Do you wish to proceed with the removal process?"):
            # Initiate the function through which the apostrophes will be replaced with user's input.
            apostrophe_killer(apostrophe_cases, grouped_results, song_data_set, change_log, change_log_double_words)
        else:
            console_data_printer("Goodbye!")

    except FileNotFoundError as e:
        print("ERROR MESSAGE: \n" + str(e))
        if str(e).__contains__("data"):
            print("The data set directory and/or the data set itself are absent! \nABORT")
        elif str(e).__contains__("result_files"):
            print("The result files directory and/or the result files themselves are absent! \nABORT")


if __name__ == "__main__":
    song_cleaner()