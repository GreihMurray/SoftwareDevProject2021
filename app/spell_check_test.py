import unittest
from .spell_check import *

class TestSpellCheckMethods(unittest.TestCase):

    def test_parse_txt(self):
        self.assertEqual(parse_txt("Here is a sentence"),
                         (['Here', ' ', 'is', ' ', 'a', ' ', 'sentence'], [0, 2, 4, 6]))
        self.assertEqual(parse_txt("single"), (['single'], [0]))
        self.assertEqual(parse_txt("I want 2 check numbers & characters"),
                         (['I', ' ', 'want', ' ', '2', ' ', 'check', ' ', 'numbers', ' ', '&', ' ', 'characters'],
                         [0, 2, 4, 6, 8, 12]))
        self.assertEqual(parse_txt("Let's test this! It is great to be @ the ballgame, with my friend!"),
                         (["Let's", ' ', 'test', ' ', 'this', '!', ' ', 'It', ' ', 'is', ' ', 'great', ' ', 'to', ' ',
                          'be', ' ', '@', ' ', 'the', ' ', 'ballgame', ',', ' ', 'with', ' ', 'my', ' ', 'friend', '!'],
                         [0, 2, 4, 7, 9, 11, 13, 15, 19, 21, 24, 26, 28]))

    def test_check_word(self):
        self.assertEqual(check_word(["Here", ' ', 'is', ' ', 'a', ' ', 'mispelled', ' ', 'word'], [0, 2, 4, 6, 8]), [6])
        self.assertEqual(check_word(['letz', ' ', 'yuse', ' ', 'compleatly', ' ', 'mispelled', ' ', 'centense'],
                                    [0, 2, 4, 6, 8]), [0, 2, 4, 6, 8])
        self.assertEqual(check_word(['Let\'z', ' ', 'test', ' ', 'this', '!', ' ', 'It', ' ', 'is', ' ', 'grait', ' ',
                                     'to', ' ', 'be', ' ', '@', ' ', 'the', ' ', 'balgame', ',', ' ', 'with', ' ', 'my',
                                    ' ', 'friend','!'], [0, 2, 4, 7, 9, 11, 13, 15, 19, 21, 24, 26, 28]), [0, 11, 21])

if __name__ == '__main__':
    unittest.main()