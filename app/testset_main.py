#!/usr/bin/env python

import argparse
import csv

from context import *
from spell_check import *
from distance_recs import *


parser = argparse.ArgumentParser()
parser.add_argument('-db', metavar='DictionaryDatabase', help='Specify JSON File which holds Dictionary DB to Test')
parser.add_argument('-ts', metavar='TestSet', help='Specify Test Set File')
parser.add_argument('-ta', metavar='TestAnswers', help='Specify Test Answers File')
parser.add_argument('-l', metavar='Language', help='Specify Language Code (ENG or IE)')
args = parser.parse_args()

test_dictDB = loadDictionary(args.db)

f = open(args.ts)
text = f.read()
word_list = text.splitlines()
f.close()

f = open(args.ts)
text = f.read()
word_list = text.splitlines()
f.close()

helper = LanguageHelper(test_dictDB, args.l)

retVal = []
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
        elif not (lower_word in test_dictDB):
            rec_unordered = helper.getSuggestionsExtra(lower_word)
            if len(rec_unordered) != 0:
                rec_ordered_probs = []
                for rec in rec_unordered:
                    if rec in test_dictDB:
                        rec_ordered_probs.append([rec, test_dictDB[rec].instances])
                rec_ordered = sort_by_count(rec_ordered_probs)
                if len(rec_ordered) != 0:
                    retVal.append([word, rec_ordered[0][0]])
                else:
                    retVal.append([word, word])
            else:
                retVal.append([word, word])
        elif not (lower_word in test_dictDB) and (toLower(word_list[idx - 1]) in test_dictDB) \
                and (toLower(word_list[idx + 1]) in test_dictDB):
            context_recs = test_dictDB[toLower(word_list[idx - 1])].getContextRecs(toLower(word_list[idx + 1]), 1)
            if len(context_recs) != 0:
                retVal.append([word, context_recs[0][0]])
            else:
                retVal.append([word, word])
        else:
            retVal.append([word, word])

with open("testSet_out.tsv","w+") as my_tsv:
    csvWriter = csv.writer(my_tsv,delimiter='\t')
    csvWriter.writerows(retVal)

my_tsv.close()