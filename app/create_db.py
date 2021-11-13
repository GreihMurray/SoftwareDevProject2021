#!/usr/bin/env python

import re
import unicodedata
from munch import DefaultMunch

from .spell_check import *
from .context import Word

def saveCharWords(rawArray, words):
    wordArray = []
    for i in words:
        if not re.search(r'[^a-zA-Z\']', rawArray[i]):
            wordArray.append(str(unicodedata.normalize('NFC', rawArray[i])).lower())
    return wordArray

def assembleDB(wordArray):
    db = {}
    for i, word in enumerate(wordArray):
        if i+2 < len(wordArray):
            if word in db:
                db[word].addContext(wordArray[i + 2], wordArray[i + 1])
            else:
                db.update({word: Word(word, context={wordArray[i + 2]: {wordArray[i + 1]: 1}})})
        elif i+1 < len(wordArray) and not isinstance(word, Word):
            db.update({word: Word(word, context={'': {wordArray[i + 1]: 1}})})
        elif not isinstance(word, Word):
            db.update({word: Word(word)})
    return db

def filterDB(db, minInstances, minConstantInst):
    for word in list(db):
        if db[word].instances < minInstances:
            del db[word]
        else:
            for aft in list(db[word].context):
                for mid in list(db[word].context[aft]):
                    if db[word].context[aft][mid] < minConstantInst:
                        del db[word].context[aft][mid]
                if not db[word].context[aft]:
                    del db[word].context[aft]

def db_to_dict(db):
    db_dict = {}
    for key in db:
        db_dict[key] = db[key].__dict__
    return db_dict

def dict_to_db(dict_db):
    db = {}
    for word in dict_db:
        db[word] = DefaultMunch.fromDict(dict_db[word])
    return db
