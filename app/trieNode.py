# The following class and functions were influenced by an article from Steve Hanov
# http://stevehanov.ca/blog/index.php?id=114

class trieNode:
    def __init__(self):
        self.word = ""
        self.children = {}

    def add_word(self, word):
        curr_node = self
        for letter in word:
            if letter not in curr_node.children:
                curr_node.children[letter] = trieNode()
            curr_node = curr_node.children[letter]

        curr_node.word = word

    def is_word(self, text):
        curr_node = self
        for letter in text:
            if letter in curr_node.children:
                curr_node = curr_node.children[letter]
            else:
                return False
        return True

def load_word_list(word_array):
    word_trie = trieNode()
    for word in word_array:
        word_trie.add_word(word)
    return word_trie

def edit_distance(trie, word, max_dist):
    curr_row = range(len(word) + 1)
    results = []

    for letter in trie.children:
        get_words(word, letter, trie.children[letter], curr_row, max_dist, results)

    return results


def get_words(word, letter, curr_node, prev_row, max_dist, results):
    columns = len(word) + 1
    curr_row = [prev_row[0] + 1]

    for column in range(1, columns):
        insert_dist = curr_row[column - 1] + 1
        delete_dist = prev_row[column] + 1

        if word[column - 1] != letter:
            replace_dist = prev_row[column - 1] + 1
        else:
            replace_dist = prev_row[column - 1]

        curr_row.append(min(insert_dist, delete_dist, replace_dist))

    if curr_row[-1] <= max_dist and curr_node.word != "":
        results.append((curr_node.word, curr_row[-1]))

    if min(curr_row) <= max_dist:
        for letter in curr_node.children:
            get_words(word, letter, curr_node.children[letter], curr_row, max_dist, results)
