from difflib import ndiff
import os, json


class ErrorModel():
    def __init__(self, letter_pairs={}):
        self.letter_pairs = letter_pairs
        self.total_pairs = 0

    def updt_lps(self, letters):
        for pair in letters:
            self.total_pairs += 1
            if pair[0] not in self.letter_pairs:
                self.letter_pairs[pair[0]] = {pair[1]: 1}
            elif pair[1] in self.letter_pairs[pair[0]]:
                self.letter_pairs[pair[0]][pair[1]] += 1
            else:
                self.letter_pairs[pair[0]][pair[1]] = 1

    def p_i_g(self, letters):
        prob = 1
        for pair in letters:
            if pair[0] in self.letter_pairs and pair[1] in self.letter_pairs[pair[0]]:
                prob = prob * (self.letter_pairs[pair[0]][pair[1]] / len(self.letter_pairs[pair[0]]))
            else:
                prob = 0
        return round(prob,4)

    def rec_list(self, given, given_prob, ed_words):
        recs = []
        if given_prob > 0:
            recs = [[given, given, given_prob]]
        for word in ed_words:
            letters = align_words(given, word[0])
            prob = round(self.p_i_g(letters)*word[1], 4)
            if prob > 0:
                recs.append([word[0], given, prob])
        return sorted(recs, key=lambda x: x[2], reverse=True)


def align_words(w1, w2):
    w1_idx = 0
    w2_idx = 0
    letter_pairs = []
    diff = list(ndiff(w1, w2))
    for i, s in enumerate(diff):
        if s[0] == ' ':
            if w2_idx < len(w2):
                letter_pairs.append([s[-1], s[-1]])
                w2_idx += 1
            else:
                letter_pairs.append([s[-1], ""])
            w1_idx += 1
        elif s[0] == '-':
            if i < (len(diff) - 1) and diff[i + 1][0] == '+':
                letter_pairs.append([s[-1], w2[w2_idx]])
                w2_idx += 1
            else:
                letter_pairs.append([s[-1], ""])
            w1_idx += 1
        elif s[0] == '+':
            if i > 0 and diff[i - 1][0] != '-':
                letter_pairs.append(["", s[-1]])
                w2_idx += 1
    return letter_pairs


def loadEM(file):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, file)
    f = open(filename, encoding='utf-8')
    text = f.read()
    f.close()

    em_dict = json.loads(text)
    error_model = ErrorModel(**em_dict)
    return error_model
