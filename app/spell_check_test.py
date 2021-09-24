import unittest
from .spell_check import *

class TestSpellCheckMethods(unittest.TestCase):

    def test_parse_txt(self):
        self.assertEqual(parse_txt("Here is a sentence"), ['Here', 'is', 'a', 'sentence'])
        self.assertEqual(parse_txt("single"), ['single'])
        self.assertEqual(parse_txt("I want 2 check numbers & characters"), ['I', 'want', '2', 'check', 'numbers', '&',
                                                                            'characters'])

    def test_check_word(self):
        self.assertEqual(check_word(["Here", 'is', 'a', 'mispelled', 'word']), [3])
        self.assertEqual(check_word(['letz', 'yuse', 'compleatly', 'mispelled', 'centense']), [0,1,2,3,4])

if __name__ == '__main__':
    unittest.main()