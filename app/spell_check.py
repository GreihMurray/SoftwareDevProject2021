import unicodedata
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

def check_word(input_list, word_list):
    print(word_list)
    check = SpellChecker()
    results = []
    for word_idx in word_list:
        if not regex.search(r'([^\p{L}\'\-])', input_list[word_idx]):
            if not check[input_list[word_idx]]:
                results.append(word_idx)
    return results


def check_other_lang(word_list, dictionary):
    results = []
    for idx, word in enumerate(word_list):
        lower_word = str(unicodedata.normalize('NFC', word)).lower()
<<<<<<< HEAD
        if lower_word not in dictionary and lower_word not in ',.!@#$/;\'':
=======
        lower_word = lower_word.strip()
        if lower_word not in dictionary and lower_word not in ',.!@#$/;:\'':
>>>>>>> 1855e9c (Bug fixes)
            results.append(idx)
    return results


def word_candidates(word_to_check):
    check = SpellChecker()
    return check.candidates(word_to_check)

<<<<<<< HEAD

def sort_by_count(word_list):
    return sorted(word_list, key=lambda x: x[1], reverse=True)
=======
def recombine(word_list):
    total_removed = 0;
    for word in word_list:
        word_index = word_list.index(word)
        if word[1] in ',.!?;:' and word != word_list[0]:
            word_list[word_index - 1][1] += word[1]
            word_list.pop(word_index)
    return word_list
>>>>>>> 1855e9c (Bug fixes)
