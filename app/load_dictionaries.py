import csv
import os

def load_dict(file):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, ('dictionaries/' + file))

    print(file)
    print(filename)
    dict = {}

    with open(filename, 'r', encoding='utf-8') as f:
        csv_read = csv.reader(f)
        for row in csv_read:
            word = row[0]
            count = row[1]
            dict[word] = count
    return dict