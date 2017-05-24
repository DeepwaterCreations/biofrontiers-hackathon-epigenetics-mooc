#!/usr/env/bin python3
import sys

import load_json

def flatten_json(data):
    """Turn the json into rows of data for csv output"""
    data_rows = []
    for student_id in data.keys():
        row = [student_id]
        student = data[student_id]

        if 'answers' in student.keys():
            for q in ['Q1', 'Q2', 'Q3', 'Q4']:
                if q in student['answers'].keys():
                    row.append(student['answers'][q])
                else:
                    row.append('NULL')
        else:
            row.extend(['NULL', 'NULL', 'NULL', 'NULL'])
            
        if 'evaluations' in student.keys():
            for evaluator_id in student['evaluations'].keys():
                row.append(evaluator_id)
                evaluation = student['evaluations'][evaluator_id]
                for score in evaluation[:17]:
                    row.append(score)
                if len(evaluation) == 18:
                    row.append(evaluation[17])
                else:
                    row.append('NULL')

        data_rows.append(row)
    return data_rows

def output_csv(data):
    """Output data in csv format to stdout"""
    for row in data:
        for i, item in enumerate(row):
            if not is_int(item) and item != "NULL":
                item = load_json.remove_garbage(item)
                row[i] = "\"{0}\"".format(item)
        print(",".join(row))

def is_int(s):
    """Returns true if the string represents an integer"""
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("USAGE: output_csv.py inputfile")
        print("Output is sent to stdout")
        sys.exit()

    data = load_json.load_data(sys.argv[1])
    data = flatten_json(data)
    output_csv(data)
