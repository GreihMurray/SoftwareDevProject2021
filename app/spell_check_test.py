import unittest
from .spell_check import *
from load_dictionaries import *
#from app.spell_check import *
#from app.load_dictionaries import *

lang_dictionaries = {}
lang_dictionaries["Irish"] = load_dict('cumulative_irish.csv')

class TestSpellCheckMethods(unittest.TestCase):

    def test_parse_txt(self):
        self.assertEqual(parse_txt("Here is a sentence"), ['Here', 'is', 'a', 'sentence'])
        self.assertEqual(parse_txt("single"), ['single'])
        self.assertEqual(parse_txt("I want 2 check numbers & characters"), ['I', 'want', '2', 'check', 'numbers', '&', 'characters'])
        self.assertEqual(parse_txt("Let's test this! It is great to be @ the ballgame, with my friend!"), ["Let's", 'test', 'this', '!', 'It', 'is', 'great', 'to', 'be', '@', 'the', 'ballgame', ',', 'with', 'my', 'friend', '!'])

    def test_check_word(self):
        self.assertEqual(check_word(["Here", 'is', 'a', 'mispelled', 'word']), [3])
        self.assertEqual(check_word(['letz', 'yuse', 'compleatly', 'mispelled', 'centense']), [0,1,2,3,4])
        self.assertEqual(check_word(['Let\'z', 'test', 'this', '!', 'It', 'is', 'grait', 'to', 'be', '@', 'the', 'balgame', ',', 'with', 'my', 'friend','!']), [0,6,11])

    def test_check_other_langs_irish(self):
        self.assertEqual(check_other_lang(['Mar', 'seo', 'a', 'deir', 'an', 'Tiarna'], lang_dictionaries['Irish']), [])
        self.assertEqual(check_other_lang(['Mrtre', 'seo', 'a', 'deir', 'an', 'Tiarna'], lang_dictionaries['Irish']), [0])
        self.assertEqual(check_other_lang(['martttr', 'SEO', 'adfdf', 'plopl', 'lokoil'], lang_dictionaries['Irish']), [0,2,3,4])
        self.assertEqual(check_other_lang(['Briathra', 'Amós', ',', 'aoire', 'de', 'chuid', 'Theacóá', '.'], lang_dictionaries['Irish']), [])
        self.assertEqual(check_other_lang(['', '', '', '', ''], lang_dictionaries['Irish']), [])
        self.assertEqual(check_other_lang(['Mar Seo', 'sEO', 'A', 'DeIr', 'tiarna an'], lang_dictionaries['Irish']), [0,4])

if __name__ == '__main__':
    unittest.main()