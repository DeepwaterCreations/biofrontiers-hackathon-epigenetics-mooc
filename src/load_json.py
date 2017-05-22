#!/usr/env/bin python3

import sys
import json

def load_data(data_filename):
    with open(data_filename) as data_file:
        data = json.load(data_file)
    return data

def clean_data(data):
    pass
    #Iterate over student ids
    #For each id, iterate over the reviews
        #For each review, slice off the comments
        #Also, divide into subsets matched to questions
    #Combine review subsets (average?)
    #Extract answers and match with combined subsets

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("USAGE: load_json.py filename")
        sys.exit()

    data = load_data(sys.argv[1])
