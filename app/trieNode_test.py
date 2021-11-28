import unittest
from .trieNode import *

class TestTrieNode(unittest.TestCase):

    def test_add_word(self):
        root = trieNode()
        root.add_word("honey")
        root.add_word("hone")
        self.assertTrue(root.is_word("honey"))
        self.assertTrue(root.is_word("hone"))

    def test_get_recs(self):
        word_array = ["bad", "band", "sad", "fruit", "orange", "bass", "said", "bed", "sand", "play", "ball", "hello"]
        test_trie = load_word_list(word_array)
        self.assertEqual(["bad"], edit_distance(test_trie, "bat", 1))
        self.assertEqual(["bad", "band", "bass", "ball", "bed", "sad"], edit_distance(test_trie, "bat", 2))
