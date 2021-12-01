#!/usr/bin/env python

import argparse
import csv

from context import *
from spell_check import *
from distance_recs import *
from trieNode import *


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

f = open(args.em, encoding='utf-8')
text = f.read()
f.close()
error_model = json.loads(text)

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
wrong_word = 0
context_error = 0
found_rec = 0
need_rec = 0
for idx, word in enumerate(word_list):
    lower_word = toLower(word)
    if args.l == "English":
        if check_word([lower_word], [0]):
            rec_unordered = word_candidates(lower_word)
            rec_ordered_probs = []
            for rec in rec_unordered:
                if rec in test_dictDB:
                    rec_ordered_probs.append([rec, test_dictDB[rec].instances])
            rec_ordered = sort_by_count(rec_ordered_probs)
            retVal.append([word, rec_ordered[0][0]])
        elif (idx != 0) and (idx != len(word_list)-1) and (toLower(word_list[idx - 1]) in test_dictDB) \
                and (toLower(word_list[idx + 1]) in test_dictDB):
            context_recs = test_dictDB[toLower(word_list[idx - 1])].getContextRecs(toLower(word_list[idx + 1]), 1)
            if len(context_recs) != 0:
                retVal.append([word, context_recs[0][0]])
            else:
                retVal.append([word, word])
        else:
            retVal.append([word, word])
    elif args.l == "Irish":
        if regex.search(r'([^\p{L}\'-])', word):
            retVal.append([word, word])
        elif lower_word not in test_dictDB:
            wrong_word += 1
            if lower_word in error_model:
                found_rec += 1
                recs = error_model[lower_word]
                retVal.append([word, recs[0][0]])
            else:
                need_rec += 1
                rec_unordered = edit_distance(word_trie, lower_word, 1)
                retVal.append([word, "?"])
            # rec_unordered = helper.getSuggestionsExtra(lower_word)
            # if len(rec_unordered) != 0:
            #     rec_ordered_probs = []
            #     for rec in rec_unordered:
            #         if rec in test_dictDB:
            #             rec_ordered_probs.append([rec, test_dictDB[rec].instances])
            #     rec_ordered = sort_by_count(rec_ordered_probs)
            #     if len(rec_ordered) != 0:
            #         retVal.append([word, rec_ordered[0][0]])
            #     else:
            #         retVal.append([word, word])
            # else:
            #     retVal.append([word, word])
        # elif (toLower(word_list[idx - 1]) in test_dictDB) and (toLower(word_list[idx + 1]) in test_dictDB):
        #     context_recs = test_dictDB[toLower(word_list[idx - 1])].getContextRecs(toLower(word_list[idx + 1]), 1)
        #     if len(context_recs) != 0:
        #         retVal.append([word, context_recs[0][0]])
        #     else:
        #         retVal.append([word, word])
        elif lower_word in error_model and (toLower(word_list[idx - 1]) in test_dictDB) and (toLower(word_list[idx + 1]) in test_dictDB):
            context_error += 1
            context_recs = test_dictDB[toLower(word_list[idx - 1])].getContextRecs(toLower(word_list[idx + 1]), 1)
            if lower_word not in context_recs and len(context_recs) != 0:
                recs = error_model[lower_word]
                if recs[0][1] > context_recs[0][1]:
                    retVal.append([word, recs[0][0]])
                else:
                    retVal.append([word, context_recs[0][0]])
            else:
                context_error -= 1
                retVal.append([word, word])
        else:
            retVal.append([word, word])

    if answer_list[idx][0] == answer_list[idx][1]:
        if retVal[idx][0] == retVal[idx][1]:
            true_neg += 1
        else:
            false_pos += 1
    else:
        if retVal[idx][0] != retVal[idx][1]:
            true_pos += 1
        else:
            false_neg += 1

        if retVal[idx][1] == answer_list[idx][1]:
            correct_rec += 1
        else:
            incorrect_rec += 1

with open("testSet_out.tsv","w+") as my_tsv:
    csvWriter = csv.writer(my_tsv,delimiter='\t')
    csvWriter.writerows(retVal)

my_tsv.close()

accuracy_recs = correct_rec / (correct_rec + incorrect_rec)
precision = true_pos / (true_pos + false_pos)
recall = true_pos / (true_pos + false_neg)
f1_score = 2 * (precision * recall) / (precision + recall)
print("Incorrect Words: " + str(wrong_word))
print("Found Rec: " + str(found_rec))
print("Need Rec: " + str(need_rec))
print("Context Error: " + str(context_error))
print("True Positive - True Negative - False Positive - False Negative")
print(str(true_pos) + " " + str(true_neg) + " " + str(false_pos) + " " + str(false_neg))
print("F1 Score: " + str(f1_score))
print("Recall: " + str(recall))
print("Precision: " + str(precision))
print("Rec Accuracy: " + str(accuracy_recs))
