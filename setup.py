#!/usr/bin/env python

from setuptools import setup

setup(
    name='song.cleaner-public_v',
    version='0.0.1',
    packages=['helpers', 'song_cleaner'],
    url='https://github.com/alevas/song.cleaner-public_v',
    license='M.I.T',
    author='Alexandros Vasileiou',
    author_email='vasil.alexandros@gmail.com',
    description='A tool for cleaning datasets', install_requires=['pandas', 'tabulate', 'nltk', 'xlrd']
)
