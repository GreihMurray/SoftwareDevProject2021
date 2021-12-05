import unicodedata
import regex
from spellchecker import SpellChecker
from .trieNode import *


def parse_txt(raw_input):
    init_word_list = regex.split(r'([^\p{L}0-9](?=\s)|[^\p{L}0-9]$|\s)', raw_input)
    input_list = []
    word_list = []
    for word in init_word_list:
        word = unicodedata.normalize('NFC', word)
        if word == ' ':
            input_list.append(word)
        elif regex.search(r'([^\p{L}\'\-])', word):
            input_list.append(word)
        elif word:
            word_list.append(len(input_list))
            input_list.append(word)
    return input_list, word_list


def check_word(word):
    check = SpellChecker()
    if not regex.search(r'([^\p{L}\'\-])', word):
        if check[word]:
            return True
    return False

def word_candidates(word_to_check):
    check = SpellChecker()
    rec_set = check.candidates(word_to_check)
    rec_list = [*rec_set, ]
    return rec_list

def sort_by_count(word_list):
    return sorted(word_list, key=lambda x: x[1], reverse=True)

def check_other_lang(input_list, word_list, dictionary):
    results = []
    for word_idx in word_list:
        if not regex.search(r'([^\p{L}\'\-])', input_list[word_idx]):
            lower_word = toLower(input_list[word_idx])
            if lower_word not in dictionary.keys():
                results.append(word_idx)
    return results


def sort_recs_by_context(recs, context, dictDB):
    prob = 0
    updt_recs = []
    if context[0] in dictDB:
        context_check = dictDB[context[0]].getContextRecs(context[1], 5)
        if len(context_check) != 0:
            context_words = list(zip(*context_check))[0]
            for word in recs:
                if word[0] in context_words:
                    prob = context_check[context_words.index(word[0])][1]
                updt_recs.append([word[0], word[1], word[2]*prob])
            return sorted(updt_recs, key=lambda x: x[2], reverse=True)
    return recs

def logicCntrl(word, context, language, dictDB, error_model, trie):
    # In Dictionary?
    correct = False
    lower_word = toLower(word)
    if language == "English":
        correct = check_word(lower_word)
    elif language == "Irish":
        correct = lower_word in dictDB

    if correct:
        # Run Through Error Model
        if len(word) <= 4:
            ed_words_tmp = edit_distance(trie, word, 1)
        elif len(word) <= 12:
            ed_words_tmp = edit_distance(trie, word, 2)
        else:
            ed_words_tmp = edit_distance(trie, word, 3)
        ed_words = []
        for ed_word in ed_words_tmp:
            ed_words.append([ed_word, dictDB[ed_word].instances])
        recs = error_model.rec_list(lower_word, dictDB[lower_word].instances, ed_words)
        sorted_recs = sort_recs_by_context(recs, context, dictDB)
        recs_list = list(zip(*sorted_recs))
        # Is word top of recs?
        if lower_word == recs[0]:
            # Yes, Correct word
            retVal = [word]
        else:
            if context[0] in dictDB:
                context_check = dictDB[context[0]].getContextRecs(context[1], 5)
                word_prob = 0
                rec_prob = 0
                if len(context_check) != 0:
                    context_words = list(zip(*context_check))[0]
                    if lower_word in context_words:
                        word_prob = context_check[context_words.index(lower_word)][1]
                    if recs_list[0] in context_words:
                        rec_prob = context_check[context_words.index(recs_list[0])][1]
                    if word_prob < rec_prob:
                        retVal = recs_list
                    else:
                        retVal = [word]
                else:
                    retVal = [word]
            # No, Incorrect & return recs
            else:
                retVal = [word]
    # Run Through Error Model
    else:
        # Return Recs
        ed_words_tmp = edit_distance(trie, lower_word, 1)
        ed_words = []
        for lower_word in ed_words_tmp:
            ed_words.append([lower_word, dictDB[lower_word].instances])
        recs = error_model.rec_list(lower_word, 0, ed_words)
        sorted_recs = sort_recs_by_context(recs, context, dictDB)
        retVal = list(zip(*sorted_recs))[0]
    return retVal


def toLower(word):
    return str(unicodedata.normalize('NFC', word)).lower()