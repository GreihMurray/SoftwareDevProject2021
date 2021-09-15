from spellchecker import SpellChecker


def parse_txt(raw_input):
    word_list = raw_input.split()
    return word_list


def check_word(word_list):
    check = SpellChecker()
    results = []
    for idx, word in enumerate(word_list):
        if not check[word]:
            results.append(idx)
    return results
