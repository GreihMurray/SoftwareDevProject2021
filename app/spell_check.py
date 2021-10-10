from spellchecker import SpellChecker
import re

def parse_txt(raw_input):
    init_word_list = re.split(r'([^a-zA-Z0-9\'])', raw_input)
    input_list = []
    word_list = []
    for word in init_word_list:
        if word == ' ':
            input_list.append(word)
        elif re.match(r'([^a-zA-Z0-9\'])',word):
            input_list.append(word)
        elif word:
            word_list.append(len(input_list))
            input_list.append(word)
    return input_list, word_list


def check_word(input_list, word_list):
    print(word_list)
    check = SpellChecker()
    results = []
    for word_idx in word_list:
        if not re.match('([^a-zA-Z0-9])', input_list[word_idx]):
            if not check[input_list[word_idx]]:
                results.append(word_idx)
    return results

def word_candidates(word_to_check):
    check = SpellChecker()
    return check.candidates(word_to_check)