import unittest
import os
from .context import *


class TestWordClass(unittest.TestCase):
    def test_init_no_args(self):
        test_word = Word("")
        self.assertEqual(test_word.text, "")
        self.assertEqual(test_word.instances, 0)

    def test_init_args(self):
        test_word = Word("apple")
        self.assertEqual(test_word.text, "apple")
        self.assertEqual(test_word.instances, 1)

    def test_setText(self):
        test_word = Word()
        test_word.setText("orange")
        self.assertEqual(test_word.text, "orange")
        test_word.setText("a2z")
        self.assertEqual(test_word.text, "a2z")
        test_word.setText("")
        self.assertEqual(test_word.text, "")
        test_word.setText("P@SS")
        self.assertEqual(test_word.text, "P@SS")

    def test_setInstances(self):
        test_word = Word()
        test_word.setInstances(1)
        self.assertEqual(test_word.instances, 1)
        test_word.setInstances(15)
        self.assertEqual(test_word.instances, 15)
        test_word.setInstances(0)
        self.assertEqual(test_word.instances, 0)
        test_word.setInstances(0.1)
        self.assertEqual(test_word.instances, 0)
        test_word.setInstances(0.9)
        self.assertEqual(test_word.instances, 0)
        test_word.setInstances(1.4)
        self.assertEqual(test_word.instances, 1)

    def test_incInstances(self):
        test_word = Word()
        test_word.incrmtInstances()
        self.assertEqual(test_word.instances, 1)
        test_word.incrmtInstances()
        self.assertEqual(test_word.instances, 2)
        test_word.setInstances(10)
        test_word.incrmtInstances()
        self.assertEqual(test_word.instances, 11)

    def test_addContext(self):
        test_word = Word("billy", context={"the": {"hates": 1}})
        self.assertEqual(test_word.context, {"the": {"hates": 1}})
        test_word.addContext("the", "climbed")
        self.assertEqual(test_word.context, {"the": {"hates": 1, "climbed": 1}})
        test_word.addContext("the", "threw")
        self.assertEqual(test_word.context, {"the": {"hates": 1, "climbed": 1, "threw": 1}})
        test_word.addContext("the", "threw")
        self.assertEqual(test_word.context, {"the": {"hates": 1, "climbed": 1, "threw": 2}})
        test_word.addContext("a", "bought")
        self.assertEqual(test_word.context, {"the": {"hates": 1, "climbed": 1, "threw": 2}, "a": {"bought": 1}})

    def test_addRecommendation(self):
        test_word = Word("boy")
        test_word.addRecommendation("toy")
        self.assertEqual(test_word.recommend, ["toy"])
        test_word.addRecommendation("bot")
        self.assertEqual(test_word.recommend, ["toy", "bot"])

    def test_getContextRecs(self):
        d = {"text": {"text": "text", "recommend": [], "instances": 1132,
                      "context": {"the": {"of": 30, "in": 5, "on": 5, "and": 3}, "center": {"align": 79},
                                  "from": {"bar": 15}, "been": {"has": 3}, "be": {"to": 4}, "and": {"messages": 7},
                                  "bar": {"bar": 10, "shift": 38}, "right": {"align": 20}, "left": {"align": 30},
                                  "text": {"bar": 40}, "Rui": {"by": 3}, "written": {"is": 4}, "a": {"as": 3},
                                  "to": {"message": 6, "messages": 4, "refers": 3},
                                  "images": {"and": 9, "may": 3, "messages": 16, "p": 3, "message": 13, "you": 6,
                                             "facebook": 21, "messaged": 13, "alternatives": 5, "appears": 4, "or": 11}}},
             "Albert": {"text": "Albert", "recommend": [], "instances": 238,
                        "context": {"rule": {"'s": 3}, "p": {"Cesare": 3}, "Herald": {"Daily": 3}}}}
        test_dict = {}
        for word in d:
            test_dict.update({word: Word(**d[word])})

        self.assertEqual(test_dict["text"].getContextRecs("to", 2), [["message", 6], ["messages", 4]])
        self.assertEqual(test_dict["text"].getContextRecs("bar", 2), [["shift", 38], ["bar", 10]])
        self.assertEqual(test_dict["text"].getContextRecs("images", 8),
                         [["facebook", 21], ["messages", 16], ["message", 13], ["messaged", 13], ["or", 11], ["and", 9],
                          ["you", 6], ["alternatives", 5]])

    def test_loadDictionary(self):
        test_dict = loadDictionary(os.getcwd() + "/app/UnitTests/dictionary_test.json")
        self.assertEqual(test_dict["text"].context, {"the": {"of": 30, "in": 5, "on": 5, "and": 3}, "center": {"align": 79}, "from": {"bar": 15}, "been": {"has": 3}, "be": {"to": 4}, "and": {"messages": 7}, "bar": {"bar": 10, "shift": 38}, "right": {"align": 20}, "left": {"align": 30}, "text": {"bar": 40}, "Rui": {"by": 3}, "written": {"is": 4}, "a": {"as": 3}, "to": {"message": 6, "messages": 4, "refers": 3}, "images": {"and": 3}, "not": {"may": 3}, "with": {"messages": 4}, "The": {"p": 3}, "or": {"message": 3}, "see": {"you": 3}, "video": {"and": 5}, "she": {"facebook": 3}, "p": {"message": 3}, "long": {"alternatives": 3}, "within": {"appears": 4}, "email": {"or": 3}})
        test_dict["text"].incrmtInstances()
        self.assertEqual(test_dict["text"].instances, 1133)