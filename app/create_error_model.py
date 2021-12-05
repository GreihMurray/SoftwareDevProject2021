#!/usr/bin/env python

import argparse
import sys

from trieNode import *
from context import *
from create_db import *
from error_model import *


def get_triples(word_array, word_trie):
    results = {}
    total = len(word_array)
    for idx, word in enumerate(word_array):
        if not (idx % 1000):
            sys.stdout.write('\r')
            sys.stdout.write(str(round(idx/total, 5)*100) + "%")
        if len(word) <= 4:
            i_words = edit_distance(word_trie, word, 1)
            results.update({word: i_words})
        elif len(word) <= 12:
            i_words = edit_distance(word_trie, word, 2)
            results.update({word: i_words})
        else:
            i_words = edit_distance(word_trie, word, 3)
            results.update({word: i_words})
    return results

def get_trip_helper(word, word_trie):
    if len(word) <= 4:
        i_words = edit_distance(word_trie, word, 1)
    elif len(word) <= 12:
        i_words = edit_distance(word_trie, word, 2)
    else:
        i_words = edit_distance(word_trie, word, 3)
    return {word: i_words}

def filter_triples(word_triples, dict_db, filt_val):
    results = {}
    for o_word, i_words in word_triples.items():
        for i_word in i_words:
            if dict_db[i_word].instances/filt_val > dict_db[o_word].instances:
                if o_word in results:
                    results[o_word].append([i_word, 0])
                else:
                    results.update({o_word: [[i_word, 0]]})
    return results

def weight_triples(word_triples, dict_db):
    results = {}
    for o_word, i_words in word_triples.items():
        if len(i_words) > 1:
            for befW, val in dict_db[o_word].context.items():
                for aftW in val.keys():
                    context_vals = []
                    for word in i_words:
                        b_context = dict_db[word[0]].context
                        if befW in b_context:
                            a_context = b_context[befW]
                            if aftW in a_context:
                                context_vals.append(a_context[aftW])
                            else:
                                context_vals.append(0)
                        else:
                            context_vals.append(0)
                    max_idx = context_vals.index(max(context_vals))
                    word_triples[o_word][max_idx][1] += 1
            for word in i_words:
                tmp_list = []
                if word[1] > 0:
                    tmp_list.append(word)
                if len(tmp_list) != 0:
                    results.update({o_word: tmp_list})
    return results


parser = argparse.ArgumentParser()
parser.add_argument('-db', metavar='DictionaryDatabase', help='Specify JSON File which holds Dictionary DB to Process.'
                                                              'This should be unfiltered to include every word found in'
                                                              'the corpus')
parser.add_argument('-wt', metavar='WeightedTriples', help='Specify JSON File with hold weighted triples for the error'
                                                           'model. This argument allow for skipping the long process of'
                                                           ' building the triples. Use this arg instead of -db.')
args = parser.parse_args()

if args.db:
    print("Load full dictionary")
    dict_db = loadDictionary(args.db)
    word_array = dict_db.keys()

    print("Create trie with all words")
    word_trie = load_word_list(word_array)

    print("Build triples")
    word_triples = get_triples(word_array, word_trie)

    print("Filter triples")
    filtered_triples = filter_triples(word_triples, dict_db, 10)

    print("Check triples context")
    weighted_triples = weight_triples(filtered_triples, dict_db)

if args.wt:
    f = open(args.db, encoding='utf-8')
    text = f.read()
    f.close()
    weighted_triples = json.loads(text)

em = ErrorModel()
for given in weighted_triples:
    for intended in weighted_triples[given]:
        letters = align_words(given, intended[0])
        em.updt_lps(letters)

print("Saving to File")
if args.db:
    out = open('weighted_triples_en.json', "w", encoding='utf-8')
    json_out = json.dumps(weighted_triples, ensure_ascii=False)
    out.write(json_out)
    out.close()

out = open('letter_pairs_en.json', "w", encoding='utf-8')
json_out = json.dumps({"letter_pairs": em.letter_pairs}, ensure_ascii=False)
out.write(json_out)
out.close()