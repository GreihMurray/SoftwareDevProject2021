import unittest
#from .spell_check import *
<<<<<<< HEAD
from app.spell_check import *
from .spell_check import *
from .load_dictionaries import *
#from app.spell_check import *
#from app.load_dictionaries import *
=======
#from .load_dictionaries import *
from app.spell_check import *
from app.load_dictionaries import *
>>>>>>> 0b1ac42 (Finishing Basic Irish Support and adding tests)

lang_dictionaries = {}
lang_dictionaries["Irish"] = load_dict('cumulative_irish.csv')

class TestSpellCheckMethods(unittest.TestCase):

    def test_parse_txt(self):
        self.assertEqual(parse_txt("Here is a sentence"),
                         (['Here', ' ', 'is', ' ', 'a', ' ', 'sentence'], [0, 2, 4, 6]))
        self.assertEqual(parse_txt("single"), (['single'], [0]))
        self.assertEqual(parse_txt("I want 2 check numbers & characters"),
                         (['I', ' ', 'want', ' ', '2', ' ', 'check', ' ', 'numbers', ' ', '&', ' ', 'characters'],
                         [0, 2, 6, 8, 12]))
        self.assertEqual(parse_txt("Let's test this! It is great to be @ the ballgame, with my friend!"),
                         (["Let's", ' ', 'test', ' ', 'this', '!', ' ', 'It', ' ', 'is', ' ', 'great', ' ', 'to', ' ',
                          'be', ' ', '@', ' ', 'the', ' ', 'ballgame', ',', ' ', 'with', ' ', 'my', ' ', 'friend', '!'],
                         [0, 2, 4, 7, 9, 11, 13, 15, 19, 21, 24, 26, 28]))
        self.assertEqual(parse_txt("Béal bocht pian géarmhíochaine leuceem géarfolaisteacha géarmhíochaine and now an "
                                   "email hi@gmail.com this & that"),
                         (["Béal", ' ', 'bocht', ' ', 'pian', ' ', 'géarmhíochaine', ' ', 'leuceem', ' ',
                           'géarfolaisteacha', ' ', 'géarmhíochaine', ' ', 'and', ' ',
                           'now', ' ', 'an', ' ', 'email', ' ', 'hi@gmail.com', ' ', 'this', ' ', '&', ' ', 'that'],
                          [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28]))

    def test_parse_text_Irish(self):
        self.assertEqual(parse_txt_other_lang('Briathra Amós, aoire de chuid Theacóá'), ['Briathra', 'Amós', ',', 'aoire', 'de', 'chuid', 'Theacóá'])
        self.assertEqual(parse_txt_other_lang('Mrtre seo a deir an Tiarna'), ['Mrtre', 'seo', 'a', 'deir', 'an', 'Tiarna'])
        self.assertEqual(parse_txt_other_lang('Fís a bhí aige faoi Iosrael i laethanta Uiziá, rí Iúdá'), ['Fís', 'a', 'bhí', 'aige', 'faoi', 'Iosrael', 'i', 'laethanta', 'Uiziá', ',', 'rí', 'Iúdá'])
        self.assertEqual(parse_txt_other_lang('agus i laethanta Iarobám mac Ióáis, rí Iosrael'), ['agus', 'i', 'laethanta', 'Iarobám', 'mac', 'Ióáis', ',', 'rí', 'Iosrael'])
        self.assertEqual(parse_txt_other_lang('dhá bhliain roimh an gcrith talún. Agus dúirt sé'), ['dhá', 'bhliain', 'roimh', 'an', 'gcrith', 'talún', '.', 'Agus', 'dúirt', 'sé'])

    def test_check_word(self):
        self.assertEqual(check_word(["Here", ' ', 'is', ' ', 'a', ' ', 'mispelled', ' ', 'word'], [0, 2, 4, 6, 8]), [6])
        self.assertEqual(check_word(['letz', ' ', 'yuse', ' ', 'compleatly', ' ', 'mispelled', ' ', 'centense'],
                                    [0, 2, 4, 6, 8]), [0, 2, 4, 6, 8])
        self.assertEqual(check_word(['Let\'z', ' ', 'test', ' ', 'this', '!', ' ', 'It', ' ', 'is', ' ', 'grait', ' ',
                                     'to', ' ', 'be', ' ', '@', ' ', 'the', ' ', 'balgame', ',', ' ', 'with', ' ', 'my',
                                    ' ', 'friend','!'], [0, 2, 4, 7, 9, 11, 13, 15, 19, 21, 24, 26, 28]), [0, 11, 21])

    def test_sort_by_count(self):
        self.assertEqual(sort_by_count([['test', 10], ['text', 12], ['other', 8], ['thing', 4]]), [['text', 12], ['test', 10], ['other', 8], ['thing', 4]])
        self.assertEqual(sort_by_count([['test', 11], ['text', 1], ['other', 4], ['thing', 9]]), [['test', 11], ['thing', 9], ['other', 4], ['text', 1]])
        self.assertEqual(sort_by_count([['test', 1], ['text', 2], ['other', 3], ['thing', 4]]), [['thing', 4], ['other', 3], ['text', 2], ['test', 1]])
        self.assertEqual(sort_by_count([['test', 10], ['text', 12], ['other', 8], ['thing', 40]]), [['thing', 40], ['text', 12], ['test', 10], ['other', 8]])
        self.assertEqual(sort_by_count([['test', 10], ['text', 10], ['other', 10], ['thing', 10]]), [['test', 10], ['text', 10], ['other', 10], ['thing', 10]])

    # def test_check_other_langs_irish(self):
    #     self.assertEqual(check_other_lang(['Mar', 'seo', 'a', 'deir', 'an', 'Tiarna'], lang_dictionaries['Irish']), [])
    #     self.assertEqual(check_other_lang(['Mrtre', 'seo', 'a', 'deir', 'an', 'Tiarna'], lang_dictionaries['Irish']), [0])
    #     self.assertEqual(check_other_lang(['martttr', 'SEO', 'adfdf', 'plopl', 'lokoil'], lang_dictionaries['Irish']), [0,2,3,4])
    #     self.assertEqual(check_other_lang(['Briathra', 'Amós', ',', 'aoire', 'de', 'chuid', 'Theacóá', '.'], lang_dictionaries['Irish']), [])
    #     self.assertEqual(check_other_lang(['', '', '', '', ''], lang_dictionaries['Irish']), [])
    #     self.assertEqual(check_other_lang(['Mar Seo', 'sEO', 'A', 'DeIr', 'tiarna an'], lang_dictionaries['Irish']), [0,4])

if __name__ == '__main__':
    unittest.main()