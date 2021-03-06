import unittest
from .spell_check import *
from .context import loadDictionary


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

    def test_check_word(self):
        self.assertTrue(check_word("here"))
        self.assertTrue(check_word("is"))
        self.assertTrue(check_word("a"))
        self.assertFalse(check_word("mispelled"))
        self.assertTrue(check_word("word"))
        self.assertFalse(check_word("letz"))
        self.assertFalse(check_word("yuse"))
        self.assertFalse(check_word("@"))
        self.assertFalse(check_word("!"))
        self.assertFalse(check_word("let\'z"))
        self.assertTrue(check_word("let\'s"))

    def test_sort_by_count(self):
        self.assertEqual(sort_by_count([['test', 10], ['text', 12], ['other', 8], ['thing', 4]]), [['text', 12], ['test', 10], ['other', 8], ['thing', 4]])
        self.assertEqual(sort_by_count([['test', 11], ['text', 1], ['other', 4], ['thing', 9]]), [['test', 11], ['thing', 9], ['other', 4], ['text', 1]])
        self.assertEqual(sort_by_count([['test', 1], ['text', 2], ['other', 3], ['thing', 4]]), [['thing', 4], ['other', 3], ['text', 2], ['test', 1]])
        self.assertEqual(sort_by_count([['test', 10], ['text', 12], ['other', 8], ['thing', 40]]), [['thing', 40], ['text', 12], ['test', 10], ['other', 8]])
        self.assertEqual(sort_by_count([['test', 10], ['text', 10], ['other', 10], ['thing', 10]]), [['test', 10], ['text', 10], ['other', 10], ['thing', 10]])

    def test_check_other_langs_irish(self):
        lang_dictionaries = {}
        lang_dictionaries['Irish'] = loadDictionary("IrishCorpus/final_irish_dictionary.json")
        input_list, word_list = parse_txt('Mar seo a deir an Tiarna')
        self.assertEqual(check_other_lang(input_list, word_list, lang_dictionaries['Irish']), [])
        input_list, word_list = parse_txt('Mrtre seo a deir an Tiarna')
        self.assertEqual(check_other_lang(input_list, word_list, lang_dictionaries['Irish']), [0])
        input_list, word_list = parse_txt('martttr SEO adfdf plopl lokoil')
        self.assertEqual(check_other_lang(input_list, word_list, lang_dictionaries['Irish']), [0, 4, 6, 8])
        # Some words in the below test do not appear in the dict due to lack of instances. If the dictionary is updated, this may change
        input_list, word_list = parse_txt('Briathra Amós , aoire de chuid Theacóá.')
        self.assertEqual(check_other_lang(input_list, word_list, lang_dictionaries['Irish']), [])
        input_list, word_list = parse_txt('     ')
        self.assertEqual(check_other_lang(input_list, word_list, lang_dictionaries['Irish']), [])

if __name__ == '__main__':
    unittest.main()
