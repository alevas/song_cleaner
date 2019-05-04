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
from song_cleaner.Apostrophe_Break import apostrophe_finder
from helpers.file_helper import json_writer
from helpers.multi_helper import query_yes_no, console_data_printer


'''S
    This method is the one which after the proper interaction with the user, replaces apostrophe words with 
    their regulars.
'''


# todo fix the user's decision tree. it has become chaotic...


def apostrophe_killer(apostrophe_cases, grouped_results, song_data_set, change_log_old, change_log_double_words):
    console_data_printer("Initializing the apostrophe_killer...")

    # this variable is used to check if the user wishes to proceed with the replacement process. It is only checked
    # after each group has been handled.
    continue_to_next_group = True
    change_log = dict()
    group_counter = len(grouped_results.keys())

    while continue_to_next_group and group_counter != 0:

        # first, we go through the groups.
        for group_id in grouped_results:

            # print all the apostrophe cases & their context belonging to the examined group
            group_case_table = []

            for apostrophe_case_id in grouped_results[group_id]["apostr_cases_ids"]:
                group_case_table.append([apostrophe_case_id,
                                         apostrophe_cases[apostrophe_case_id]["apostr_word"],
                                         apostrophe_cases[apostrophe_case_id]['song_id'],
                                         apostrophe_cases[apostrophe_case_id]['position'],
                                         apostrophe_cases[apostrophe_case_id]['word-2'],
                                         apostrophe_cases[apostrophe_case_id]['word-1'],
                                         apostrophe_cases[apostrophe_case_id]['word+1'],
                                         apostrophe_cases[apostrophe_case_id]['word+2']])
            message = "There are " + str(group_counter) + " groups remaining. Currently at group: " + str(group_id)
            console_data_printer(message, group_case_table,
                                 ["id", "word", "song ID", "position", "word-2", "word-1", "word+1", "word+2"])

            # The following structure ensures that the user's input will be numbers that are song id's of the
            # current group.
            checker = False
            while not checker:
                try:
                    list_to_replace = input("Choose the apostrophe id's you wish to fix: ")

                    # FEATURE: If the user types 'all', all available apostrophe cases are selected.
                    if list_to_replace in ('all', 'αλλ', 'ALL', 'ΑΛΛ'):
                        list_to_replace = grouped_results[group_id]["apostr_cases_ids"]
                        checker = True
                    else:
                        list_to_replace = ["apostrophe_" + x for x in list_to_replace.split(",")]
                        while list_to_replace and set(list_to_replace).issubset(
                                grouped_results[group_id]["apostr_cases_ids"]):

                            # ensure that if the user gave the same number as an input twice

                            list_to_replace = list(set(list_to_replace))
                            list_to_replace.sort()
                            checker = True
                            break
                        else:
                            # todo string formatting
                            raise ValueError("Please choose from: " + ''.join(
                                x for x in grouped_results[group_id]["apostr_cases_ids"]))

                except ValueError as e:
                    print("The input you gave is not acceptable... Try again.\nError message: ", str(e), "\n")

            print("You chose songs :", list_to_replace, sep='\n')
            checker = query_yes_no("Are you sure?")

            if checker:
                replace_with = input("Insert text that will replace word with apostrophe: ")
                while not isinstance(replace_with, (str,)):
                    print("You gave something other than a string!")
                    replace_with = input("Insert text that will replace word with apostrophe: ")
                # todo enchancement: chek for hamming distance and if the user's input has nothing to do with the word,
                # do not allow the value to pass
                print("You chose the word : ", replace_with)

                # If two words had to be split, they would insert an empty space between them, so we split it
                if ' ' in replace_with:
                    replace_with = [x for x in replace_with.split(" ")]

                checker = query_yes_no("Are you sure?")

                # this is where the replacement process takes part
                if checker:
                    group_counter -= 1
                    for i in list_to_replace:

                        change_log[i] = {"group_id": group_id,
                                         "apostr_case": grouped_results[group_id]["apostr_case"],
                                         "to_replace": replace_with,
                                         "song_id": apostrophe_cases[i]["song_id"],
                                         "position": apostrophe_cases[i]["position"],
                                         "word-2": apostrophe_cases[i]["word-2"],
                                         "word-1": apostrophe_cases[i]["word-1"],
                                         "word+1": apostrophe_cases[i]["word+1"],
                                         "word+2": apostrophe_cases[i]["word+2"]}

                        # if the replace_with variable has two words in it, it means that the apostrophe case was
                        # of the type (word)'(word), so they had to be split. We need to update other apostrophe
                        # cases, because each word's id changes by 2
                        song_id = apostrophe_cases[i]["song_id"]
                        word_position = apostrophe_cases[i]["position"]
                        if isinstance(replace_with, (list,)):

                            song_data_set[song_id]["lyrics"][word_position] = replace_with[0]
                            song_data_set[song_id]["lyrics"].insert(word_position + 1, replace_with[1])

                            # Here we check if there are other apostrophe cases that have words with apostrophes
                            # to adjust the word id's with the change (shift by 1). This will only happen for words
                            # with equal or bigger song id than that of the word changed
                            for case in apostrophe_cases:

                                if song_id == apostrophe_cases[case]["song_id"] and \
                                                word_position < apostrophe_cases[case]["position"]:

                                    double_case_id = i
                                    while double_case_id in change_log_double_words:
                                        double_case_id += "+"

                                    change_log_double_words[double_case_id] = {"apostr_case": apostrophe_cases[case]["apostr_word"],
                                                                   "song_id": apostrophe_cases[case]["song_id"],
                                                                   "position_old": apostrophe_cases[case]["position"],
                                                                   "position_new": apostrophe_cases[case][
                                                                                       "position"] + 1}
                                    apostrophe_cases[case]["position"] += 1

                        else:
                            song_data_set[song_id]["lyrics"][word_position] = replace_with
                else:
                    print("You can proceed with another group.")

            else:
                print("You just jumped group ", group_id)
            continue_to_next_group = query_yes_no("Do you wish to continue?")
            if not continue_to_next_group:
                break

    else:
        if not group_counter:
            print("It seems there are no more groups remaining!")
    if change_log:

        console_data_printer('Words that changed', change_log, change_log)
        if change_log_double_words:
            console_data_printer('Words whose ID changes due to changes in other words',
                                 change_log_double_words, change_log_double_words)

        if query_yes_no("Do you want to write these changes?"):
            for i in change_log:
                group_id = change_log[i]["group_id"]
                apostr_case = i
                grouped_results[group_id]["apostr_cases_ids"].remove(apostr_case)
                if len(grouped_results[group_id]["apostr_cases_ids"]) == 0:
                    del grouped_results[group_id]
                del apostrophe_cases[apostr_case]

            # we have to do this to ensure that the files we wish to write to do not keep junk from other runs.
            # file_helper.file_cleaner()

            change_log_old.update(change_log)
            for i, j in zip([apostrophe_cases, grouped_results, song_data_set, change_log_old, change_log_double_words],
                            ['apostrophe_cases', 'grouped_results', 'song_data_set', 'change_log',
                             'change_log_double_words']):
                json_writer(i, j)

            print("\nChanges saved at the following files:\n"
                  "apostrophe_cases\n"
                  "grouped_results\n"
                  "song_data_set\n"
                  "change_log\n"
                  "change_log_double_words")
        else:
            print("No changes will be saved.")
    else:
        print("No changes made!")
    console_data_printer("The apostrophe_killer will now terminate.")


if __name__ == "__main__":
    console_data_printer("The Apostrophe_Eliminator has been called as standalone. This is not advised!")
    console_data_printer("WARNING: IF YOU PROCEED, PREVIOUS DATA WILL BE OVERWRITTEN!")
    if query_yes_no("Do you still wish to proceed?"):
        t1, t2, t3 = apostrophe_finder()
        apostrophe_killer(t1, t2, t3)
    else:
        console_data_printer("...Aborting...")
