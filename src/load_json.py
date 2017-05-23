#!/usr/env/bin python3
import sys
import json

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
            reviewer_scores = [reviewer_scores[:7], reviewer_scores[7:11], reviewer_scores[11:14], reviewer_scores[14:]]
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
        for i, q in enumerate(['Q1', 'Q2', 'Q3', 'Q4']):
            if q in answers:
                cleaned_data.append([answers[q]] + scores[i])
            
    return cleaned_data


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("USAGE: load_json.py filename")
        sys.exit()

    data = load_data(sys.argv[1])
    cleaned_data = clean_data(data)
