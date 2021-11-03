import unicodedata
from spellchecker import SpellChecker
import re

def parse_txt(raw_input):
    init_word_list = re.split('([^a-zA-Z0-9\'])', raw_input)
    word_list = []
    for word in init_word_list:
        if word != ' ' and word:
            word_list.append(word)
    return word_list

def parse_txt_other_lang(raw_input):
    init_word_list = re.split(' ', raw_input)
    word_list = []
    for word in init_word_list:
        if word and word != ' ':
            if word[-1] in '\.\?!,;_:%“”\' …\+"’‘':
                word_list.append(word[0:len(word)-1])
                word_list.append(word[-1])
            else:
                word_list.append(word)
    return word_list

def check_word(word_list):
    check = SpellChecker()
    results = []
    for idx, word in enumerate(word_list):
        if not re.match('([^a-zA-Z0-9])', word):
            if not check[word]:
                results.append(idx)

    return results

def check_other_lang(word_list, dictionary):
    results = []
    for idx, word in enumerate(word_list):
        lower_word = str(unicodedata.normalize('NFC', word)).lower()
        lower_word = lower_word.strip()
        if lower_word not in dictionary and lower_word not in ',.!@#$/;:\'':
            results.append(idx)
    return results

def word_candidates(word_to_check):
    check = SpellChecker()
    return check.candidates(word_to_check)

def recombine(word_list):
    for word in word_list:
        word_index = word_list.index(word)
        print(word_list)
        print('/////////////////////////', word)
        if word[1] in ',.!;:' and word != word_list[0]:
            word_list[word_index - 1][1] += word[1]
            word_list.pop(word_index)
    return word_list