import csv
import os
import re

directory = 'irish'
files = []

for filename in os.listdir(directory):
    print(os.path.join(directory, filename))
    files.append(os.path.join(directory, filename))

all_words = []

for file in files:
    with open(file, encoding='utf8') as f:
        i = 1
        lines = f.readlines()
        for line in lines:
            words = re.split('\.|\?|!|,|\n|\t|;|\(|\)|\[|]|\{|}|_|:|\*|/|\|@|&|%|$|#|“|”|\'| |…|\+|"|’|‘|=| ', line)
            for word in words:
                if word and word != '-':
                    all_words.append(word)
            print('Line ', i, ' of ', len(lines), ' in ', file, ': ', line)
            i += 1

with open('irish_corpus.txt', 'w', encoding='utf-8', newline='') as f:
    f.write(str(all_words))
    print(word)