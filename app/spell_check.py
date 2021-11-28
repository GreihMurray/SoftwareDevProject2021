import unicodedata

from spellchecker import SpellChecker
from .distance_recs import *
import regex

def parse_txt(raw_input):
    init_word_list = regex.split(r'([^\p{L}0-9](?=\s)|[^\p{L}0-9]$|\s)', raw_input)
    input_list = []
    word_list = []
    for word in init_word_list:
        if word == ' ':
            input_list.append(word)
        elif regex.search(r'([^\p{L}\'\-])', word):
            input_list.append(word)
        elif word:
            word_list.append(len(input_list))
            input_list.append(word)
    return input_list, word_list


def check_word(input_list, word_list):
    check = SpellChecker()
    results = []
    for word_idx in word_list:
        if not regex.search(r'([^\p{L}\'\-])', input_list[word_idx]):
            if not check[input_list[word_idx]]:
                results.append(word_idx)
    return results

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

def logicCntrl(inptTxt, language, dictDB):
    retWords = []
    retRecs = []

    helper = LanguageHelper(dictDB[language], language)

    input_list, word_list = parse_txt(inptTxt)

    for wordIdx, token in enumerate(input_list):
        if wordIdx in word_list:
            lower_word = toLower(input_list[wordIdx])
            idx = word_list.index(wordIdx)
            print(lower_word)
            if language == "English":
                if check_word([lower_word], [0]):
                    rec_unordered = word_candidates(lower_word)
                    rec_ordered_probs = []
                    for rec in rec_unordered:
                        if rec in dictDB["English"]:
                            rec_ordered_probs.append([rec, dictDB["English"][rec].instances])
                    rec_ordered = sort_by_count(rec_ordered_probs)
                    retWords.append(('Misspelled_words', input_list[wordIdx]))
                    retRecs.append((input_list[wordIdx], [row[0] for row in rec_ordered][:5]))
                elif (idx != 0) and (idx != len(word_list) - 1) and (toLower(input_list[word_list[idx - 1]]) in dictDB["English"]) \
                        and (toLower(input_list[word_list[idx + 1]]) in dictDB["English"]):
                    print("in here - " + input_list[word_list[idx - 1]] + " " + input_list[word_list[idx + 1]])
                    context_recs = dictDB["English"][toLower(input_list[word_list[idx - 1]])].getContextRecs(toLower(input_list[word_list[idx + 1]]), 5)
                    if (len(context_recs) != 0) and not (input_list[wordIdx] in [row[0] for row in context_recs]):
                        retWords.append(('Recommendation_words', input_list[wordIdx]))
                        retRecs.append((input_list[wordIdx], [row[0] for row in context_recs]))
                    else:
                        retWords.append(('', input_list[wordIdx]))
                else:
                    print("how about here")
                    retWords.append(('', input_list[wordIdx]))
            elif language == "Irish":
                if not (lower_word in dictDB["Irish"]):
                    rec_unordered = helper.getSuggestionsExtra(lower_word)
                    rec_ordered_probs = []
                    for rec in rec_unordered:
                        if rec in dictDB["Irish"]:
                            rec_ordered_probs.append([rec, dictDB["Irish"][rec].instances])
                    rec_ordered = sort_by_count(rec_ordered_probs)
                    retWords.append(('Misspelled_words', input_list[wordIdx]))
                    retRecs.append((input_list[wordIdx], [row[0] for row in rec_ordered][:5]))
                elif (idx != 0) and (idx != len(word_list) - 1) and (toLower(input_list[word_list[idx - 1]]) in dictDB["Irish"]) \
                        and (toLower(input_list[word_list[idx + 1]]) in dictDB["Irish"]):
                    context_recs = dictDB["Irish"][toLower(input_list[word_list[idx - 1]])].getContextRecs(toLower(input_list[word_list[idx + 1]]), 10)
                    if len(context_recs) != 0 and not (input_list[wordIdx] in [row[0] for row in context_recs]):
                        retWords.append(('Recommendation_words', input_list[wordIdx]))
                        retRecs.append((input_list[wordIdx], [row[0] for row in context_recs][:5]))
                    else:
                        retWords.append(('', input_list[wordIdx]))
                else:
                    retWords.append(('', input_list[wordIdx]))
        else:
            retWords.append(('', input_list[wordIdx]))

    return input_list, word_list, retWords, retRecs


def toLower(word):
    return str(unicodedata.normalize('NFC', word)).lower()