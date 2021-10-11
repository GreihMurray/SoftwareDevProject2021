from spellchecker import SpellChecker
import re


def parse_txt(raw_input):
    init_word_list = re.split('([^a-zA-Z0-9\'])', raw_input)
    word_list = []
    for word in init_word_list:
        if word != ' ' and word:
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
