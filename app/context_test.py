import unittest
from .context import *


class TestWordClass(unittest.TestCase):
    def test_init_no_args(self):
        test_word = Word()
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
        test_word = Word("billy", "the", "hates")
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