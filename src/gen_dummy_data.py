#!/usr/bin/env python3
import random
import json

word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()

def gen_text(length):
    """Return a string of 'length' random words"""
    s = [random.choice(WORDS) for i in range(length)]
    return " ".join(s)

def gen_id_list(length):
    """Return a list of 'length' random ints"""
    return [random.randint(1000000, 9999999) for i in range(length)]

def get_student_obj():
    student_obj = {}
    student_obj['evaluations'] = {}
    for evaluator_id in gen_id_list(random.randint(1,4)):
        student_obj['evaluations'][evaluator_id] = [str(random.randint(0,2)) for i in range(17)]
        student_obj['evaluations'][evaluator_id] += [gen_text(140)]

    student_obj['answers'] = {}
    for q in ['Q1', 'Q2', 'Q3', 'Q4']:
        student_obj['answers'][q] = gen_text(256)
    return student_obj


if __name__ == "__main__":
    json_obj = {}
    for id in gen_id_list(300):
        json_obj[str(id)] = get_student_obj()
    print(json.dumps(json_obj))
