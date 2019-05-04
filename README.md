# song.cleaner

This is a command line tool that was originally developed to replace apostrophed words with their non-apostrophed version on Greek songs. Eg. the words "do" and "not" can be written as "don't". If data analysis/machine learning techniques are performed on a dataset containing that case (NLP), "don't" appears as a different word than "do" and "not". Therefore, it should somehow be replaced by the original words.

In short, the project does the following:
1. parse a given dataset
2. tokenize each song, remove specified punctuation marks, find apostrophe cases and group them
3. print a group and accept the user's input as the word that will replace the apostrophe case
4. save changes as well as log the performed changes.

## Getting Started


### Prerequisites

What things you need to install the software and how to install them
This project runs on Python 3 (version>3.5).

#### Anaconda
Python Anaconda with Python3 and above version 3.5 should be working.

#### Alternatively

##### Packages:

Run the 
```
setup.py
```
which will install packages:
* [Pandas](https://pandas.pydata.org/)
* [Tabulate](https://pypi.org/project/tabulate/)
* [NLTK](https://www.nltk.org/)
* [XLRD](https://pypi.org/project/xlrd/)


which are necessary to run this project. Else, manual download is always an option.

To have them installed on your system.

### Usage

Data sets to be examined should be stored in the /data folder in .xlsx format. Please see the given samples (in English and Greek).

The tool has two main sections, which do the following: 

#### 1. Analyse the given data set, tokenize it and find all apostrophe cases.

```
apostrophe_cases.json
grouped_results.json	
song_data_set.json
```
are then generated. They contain

a. the apostrophe cases, each with the case ID, the song ID, the position in the song and its context (two words before and after the word). Eg:

    "apostrophe_0000": {
        "apostr_word": "don't",
        "song_id": "song_0000",
        "position": 11,
        "word-2": "",
        "word-1": "please",
        "word+1": "take",
        "word+2": "my"
    }


     
 b. the grouped results, which are the above apostrophe cases grouped. Each group has a unique ID, the apostrophe case itself, it's frequency and the apostrophe case IDs to mach with the file above. Eg:
 
 ```
 "group_0004": {
    "apostr_case": "don't",
    "frequency": 2,
    "apostr_cases_ids": [
        "apostrophe_6639",
        "apostrophe_6641"
    ]
}
```

 c. the (now tokenized) data set.
 
#### 2. Present the user with the first apostrophe case group and the apostrophe case's information, as well as how many more groups are remaining. 
Eg:

```
====================================================================================================
*******************There are 980 groups remaining. Currently at group: group_0004*******************
====================================================================================================

id               word    song ID      position  word-2    word-1    word+1    word+2
---------------  ------  ---------  ----------  --------  --------  --------  --------
apostrophe_6639  he's  song_1971           0                        done            it
apostrophe_6641  it's  song_1971          58      they     say    never       over
====================================================================================================
```


which helps the user determine which word(s) will replace the apostrophe case.

Then the user can choose the groups he wished to change by giving the apostrophe case ID as input. Giving the words 'all', 'αλλ', 'ALL', 'ΑΛΛ' will have all the apostrophe cases as selected. A partial selection can be useful when the user is not too sure over certain cases or if the actual words are not the same. After each group, the user is asked if they wish to proceed to the next group. If not, the changes are printed and the user is prompted to save them.

Changes on *apostrophe_cases.json*, *grouped_results.json* and *song_data_set.json* are saved and the following logging files are created in the *result_files* folder:

```
change_log.json	
change_log_double_words.json
```
The *change_log.json* file contains all the changes performed on apostrophe cases. The *change_log_double_words.json* contains all the "collateral" damage to words in a song due to the fact that eg. the word "don't" breaks in "do" and "not", which means that any apostrophe case after that word will be shifted by 1, so it's apostrophe ID has to change to replace the correct word in the song.



The flow of Song_Cleaner_Project.py is the following:

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
        
**IMPORTANT NOTICE OVER EXCEL DATASHEETS**

Since there is a certain issue when .xlsx files opened previously by excel, please check the written song_data_set.txt for any encoding errors. It usually looks like this: "\\\\\x91". Be extra careful not to cause changes to the order of the song's apostrophe marked words, which would cause extreme problems when trying to replace them.     
## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/alevas/song.cleaner-public_v/tags). 

## Authors

* **Alexandros Vasileiou** - *Initial work* - [alevas](https://github.com/alevas)

See also the list of [contributors](https://github.com/alevas/song.cleaner-public_v/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENCE](LICENCE) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
    * To the NTLK team who have done a great job.
    * The open source community who are always there when you need them.
* Inspiration
    * [Thomas Asikis](https://github.com/asikist), without whom this project might have never existed.
* Also
    * Coffee makers who keep us up and running.
