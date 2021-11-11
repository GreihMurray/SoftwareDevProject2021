import unittest
from .create_db import *


class TestCreateDBMethods(unittest.TestCase):
    def test_saveCharWords(self):
        self.assertEqual(saveCharWords(['Here', ' ', 'is', ' ', 'a', ' ', 'sentence'], [0, 2, 4, 6]),
                         ['Here', 'is', 'a', 'sentence'])
        self.assertEqual(saveCharWords(['single'], [0]), ['single'])
        self.assertEqual(parse_txt("I want 2 check numbers & characters"),
                         (['I', ' ', 'want', ' ', '2', ' ', 'check', ' ', 'numbers', ' ', '&', ' ', 'characters'],
                         [0, 2, 6, 8, 12]))
        self.assertEqual(saveCharWords(["Let's", ' ', 'test', ' ', 'this', '!', ' ', 'It', ' ', 'is', ' ', 'great', ' ',
                                        'to', ' ','be', ' ', '@', ' ', 'the', ' ', 'ballgame', ',', ' ', 'with', ' ',
                                        'my', ' ', 'friend', '!'],
                         [0, 2, 4, 7, 9, 11, 13, 15, 19, 21, 24, 26, 28]), ["Let's", 'test', 'this', 'It', 'is', 'great',
                                        'to', 'be', 'the', 'ballgame', 'with', 'my', 'friend'])
        self.assertEqual(saveCharWords(['an',' ', 'email', ' ', 'address', ':', ' ', 'Email@goog.com'], [0, 2, 4, 7]),
                         ['an','email', 'address'])

    def test_assembleDB(self):
        test_db = assembleDB(['here', 'is', 'a', 'sentence', 'there', 'are', 'repeats', 'this', 'is', 'a', 'test'])
        self.assertEqual({'a': {'is': 1}}, test_db['here'].context)
        self.assertEqual(1, test_db['here'].instances)
        self.assertEqual({'sentence': {'a': 1}, 'test': {'a': 1}}, test_db['is'].context)
        self.assertEqual({'are': {'there': 1}}, test_db['sentence'].context)
        self.assertEqual(2, test_db['is'].instances)

    def test_filterDB(self):
        test_db = assembleDB(['here', 'is', 'a', 'sentence', 'there', 'are', 'repeats', 'this', 'is', 'a', 'test',
                              'we', 'want', 'there', 'to', 'be', 'repeat', 'sentence', 'so', 'that', 'there', 'can',
                              'be', 'a', 'test', 'it', 'is', 'a', 'test', 'there', 'to', 'be'])
        filterDB(test_db, 2, 2)
        self.assertEqual({'test': {'a': 2}}, test_db['is'].context)
        self.assertEqual(3, test_db['is'].instances)
        self.assertEqual(False, 'here' in test_db)
        self.assertEqual(False, 'want' in test_db)
        self.assertEqual({'be': {'to': 2}}, test_db['there'].context)
        self.assertEqual(4, test_db['there'].instances)

if __name__ == '__main__':
    unittest.main()