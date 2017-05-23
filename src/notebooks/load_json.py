#!/usr/env/bin python3
import sys
import json
from html.parser import HTMLParser

import numpy as np

def load_data(data_filename):
    with open(data_filename) as data_file:
        data = json.load(data_file)
    return data

def clean_data(data):
    """Strip garbage from data and reorganize

    Output: A list of sublists, where each sublist is a student's answer to one question followed by
    the averages of the scores given to that question by the student's reviewers.
    """
    # questions = ['Q1', 'Q2', 'Q3', 'Q4']
    questions = ['Q1']
    cleaned_data = []
    #Iterate over student ids
    for student_id in data.keys():
        scores = []
        if 'answers' not in data[student_id] or \
            'evaluations' not in data[student_id] or \
            data[student_id]['answers'] == {}:
            continue
        #For each id, iterate over the reviews
        for reviewer in data[student_id]['evaluations'].values():
            #For each review, slice off the comments
            reviewer_scores = reviewer[:17]
            #Also, divide into subsets matched to questions
            reviewer_scores = [reviewer_scores[:6], reviewer_scores[6:10], reviewer_scores[10:13], reviewer_scores[13:]]
            #Turn strings into ints
            for q in range(len(reviewer_scores)):
                reviewer_scores[q] = list(map(int, reviewer_scores[q]))
            #Average the new scores into the existing list
            if scores == []:
                scores = reviewer_scores
            else:
                for q in range(len(scores)):
                    scores[q] = [np.mean(list(s)) for s in zip(scores[q], reviewer_scores[q])]

        #Extract answers and match with combined subsets
        answers = data[student_id]['answers']
        for i, q in enumerate(questions):
            if q in answers:
                answer = remove_garbage(answers[q])
                cleaned_data.append([answer] + scores[i])
            
    return cleaned_data

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return "".join(self.fed)

def remove_garbage(s):
    """Strip html and unicode artifacts from string s"""
    #HTML
    html_stripper = HTMLStripper()
    html_stripper.feed(s)
    s = html_stripper.get_data()

    #Unicode and unparsed newlines
    s = bytes(s, "utf-8").decode("ascii", "ignore")
    s = s.replace('\n', ' ')

    return s

def normalize_scores(y):
    """Return a list of normalized scores between 0.0 and 1.0"""
    max_val = max(y)
    return [y_val/max_val for y_val in y]

def get_features(filename, normalize_y = False):
    """Return (x, y) where x is a list of answers to Q1, and y is a list of sums over the averaged score array
    for that answer
    """
    data = load_data(filename)
    cleaned_data = clean_data(data)
    x = [d[0] for d in cleaned_data]
    y = [sum(d[1:]) for d in cleaned_data]
    if normalize_y:
        y = normalize_scores(y)
    return (x, y)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("USAGE: load_json.py filename")
        sys.exit()

    x, y = get_features(sys.argv[1])
    for row in zip(x, y):
        print(row)
