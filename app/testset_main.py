#!/usr/bin/env python

import argparse
import csv

from context import *
from spell_check import *
from distance_recs import *
from trieNode import *
from error_model import *


parser = argparse.ArgumentParser()
parser.add_argument('-db', metavar='DictionaryDatabase', help='Specify JSON File which holds Dictionary DB to Test')
parser.add_argument('-em', metavar='ErrorModel', help='Specify JSON File which holds the Error Model to Test')
parser.add_argument('-ts', metavar='TestSet', help='Specify Test Set File')
parser.add_argument('-ta', metavar='TestAnswers', help='Specify Test Answers File')
parser.add_argument('-l', metavar='Language', help='Specify Language Code (ENG or IE)')
args = parser.parse_args()

test_dictDB = loadDictionary(args.db)

f = open(args.ts)
text = f.read()
word_list = text.splitlines()
f.close()

error_model = loadEM(args.em)

f = open(args.ta)
text_ans = f.read()
f.close()

answer_lines = text_ans.splitlines()
answer_list = []
for line in answer_lines:
    temp_ans = line.split('\t')
    if len(temp_ans) == 1:
        temp_ans.append('')
    answer_list.append(temp_ans)

helper = LanguageHelper(test_dictDB, args.l)

word_array = test_dictDB.keys()
word_trie = load_word_list(word_array)

retVal = []
true_pos = 0
true_neg = 0
false_pos = 0
false_neg = 0
correct_rec = 0
incorrect_rec = 0
c_err = 0
context_err = False
for idx, word in enumerate(word_list):
    if regex.search(r'([^\p{L}\'-])', word):
        retVal.append([word, word])
    else:
        if idx != 0:
            prevW = toLower(word_list[idx-1])
        else:
            prevW = ""
        if idx != len(word_list)-1:
            aftW = toLower(word_list[idx+1])
        else:
            aftW = ""
        recs, context_err = logicCntrl(word, [prevW, aftW], args.l, test_dictDB, error_model, word_trie)
        retVal.append([word, recs[0]])

    if answer_list[idx][0] == answer_list[idx][1]:
        if retVal[idx][0] == retVal[idx][1]:
            true_neg += 1
        else:
            false_pos += 1
            if context_err:
                c_err += 1
    else:
        if retVal[idx][0] != retVal[idx][1]:
            true_pos += 1
            if context_err:
                c_err += 1
        else:
            false_neg += 1

        if retVal[idx][1] == answer_list[idx][1]:
            correct_rec += 1
        else:
            incorrect_rec += 1

with open("testSet_out.tsv","w+") as my_tsv:
    csvWriter = csv.writer(my_tsv, delimiter='\t')
    csvWriter.writerows(retVal)

my_tsv.close()

accuracy_recs = correct_rec / (correct_rec + incorrect_rec)
precision = true_pos / (true_pos + false_pos)
recall = true_pos / (true_pos + false_neg)
f1_score = 2 * (precision * recall) / (precision + recall)
print("Context Misspellings: " + str(c_err))
print("True Positive - True Negative - False Positive - False Negative")
print(str(true_pos) + " " + str(true_neg) + " " + str(false_pos) + " " + str(false_neg))
print("F1 Score: " + str(f1_score))
print("Recall: " + str(recall))
print("Precision: " + str(precision))
print("Rec Accuracy: " + str(accuracy_recs))
