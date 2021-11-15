#!/usr/bin/env python

import json
import argparse
from create_db import *


parser = argparse.ArgumentParser()
parser.add_argument('-p', metavar='ParseText', nargs='+', help='Parse given files to create list of words')
parser.add_argument('-d', metavar='CreateDictionary', help='Create dictionary with given file of words.')
parser.add_argument('-f', metavar='FilterDictionary', nargs='+', help="Filter given dictionary based on given values (i.e. -f 'filename' minInstances"
                                          "minContextInstances")
args = parser.parse_args()

if args.p:
    wordArray = []
    for file in args.p:
        f = open(file, encoding='utf-8')
        text = f.read()
        f.close()

        rawArray, words = parse_txt(text)
        wordArray += saveCharWords(rawArray, words)

    out = open('output.json', "w", encoding='utf-8')
    json_wordArray = json.dumps(wordArray, ensure_ascii=False)
    out.write(json_wordArray)
    out.close()

if args.d:
    f = open(args.d, encoding='utf-8')
    text = f.read()
    f.close()

    wordArray = json.loads(text)
    db = assembleDB(wordArray)

    db_dict = db_to_dict(db)

    out = open('db_output.json', "a", encoding='utf-8')
    json_db = json.dumps(db_dict, ensure_ascii=False)
    out.write(json_db)
    out.close()

if args.f:
    f = open(args.f[0], encoding='utf-8')
    text = f.read()
    f.close()

    db_dict = json.loads(text)
    db = dict_to_db(db_dict)

    filterDB(db, int(args.f[1]), int(args.f[2]))

    out = open('filtered_db_output.json', "a", encoding='utf-8')
    json_db = json.dumps(db, ensure_ascii=False)
    out.write(json_db)
    out.close()