from spellchecker import SpellChecker
import regex

def parse_txt(raw_input):
    init_word_list = regex.split(r'([^\p{L}0-9](?=\s)|[^\p{L}0-9]$|\s)', raw_input)
    print(init_word_list)
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
    print(word_list)
    check = SpellChecker()
    results = []
    for word_idx in word_list:
        if not regex.search(r'([^\p{L}\'\-])', input_list[word_idx]):
            if not check[input_list[word_idx]]:
                results.append(word_idx)
    return results

def word_candidates(word_to_check):
    check = SpellChecker()
    return check.candidates(word_to_check)

def sort_by_count(word_list):
    return sorted(word_list, key=lambda x: x[1], reverse=True)