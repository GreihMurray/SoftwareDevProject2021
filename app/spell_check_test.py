import unittest
from .spell_check import *

class TestSpellCheckMethods(unittest.TestCase):

    def test_parse_txt(self):
        self.assertEqual(parse_txt("Here is a sentence"), ['Here', 'is', 'a', 'sentence'])
        self.assertEqual(parse_txt("single"), ['single'])
        self.assertEqual(parse_txt("I want 2 check numbers & characters"), ['I', 'want', '2', 'check', 'numbers', '&',
                                                                            'characters'])
<<<<<<< HEAD
        self.assertEqual(parse_txt("Let's test this! It is great to be @ the ballgame, with my friend!"), ["Let's", 'test', 'this', '!', 'It', 'is', 'great', 'to', 'be', '@', 'the', 'ballgame', ',', 'with', 'my', 'friend', '!'])
=======
>>>>>>> 8863bbc (Flask web dev to InputOutputRework (#10))

    def test_check_word(self):
        self.assertEqual(check_word(["Here", 'is', 'a', 'mispelled', 'word']), [3])
        self.assertEqual(check_word(['letz', 'yuse', 'compleatly', 'mispelled', 'centense']), [0,1,2,3,4])
<<<<<<< HEAD
        self.assertEqual(check_word(['Let\'z', 'test', 'this', '!', 'It', 'is', 'grait', 'to', 'be', '@', 'the', 'balgame', ',', 'with', 'my', 'friend','!']), [0,6,11])
=======
>>>>>>> 8863bbc (Flask web dev to InputOutputRework (#10))

if __name__ == '__main__':
    unittest.main()