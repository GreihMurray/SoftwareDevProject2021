import unittest
from .error_model import *

class TestSpellCheckMethods(unittest.TestCase):

    def test_udpt_lps(self):
        test_model = ErrorModel()
        test_model.updt_lps([["e", "e"], ["w", "w"], ["e", ""]])
        self.assertEqual(test_model.letter_pairs, {"e": {"e": 1, "": 1}, "w": {"w": 1}})
        test_model.updt_lps([["a", "e"], ["e", "w"], ["", "b"], ["w", "w"]])
        self.assertEqual(test_model.letter_pairs,
                         {"e": {"e": 1, "": 1, "w": 1}, "w": {"w": 2}, "a": {"e": 1}, "": {"b": 1}})

    def test_pig(self):
        test_model = ErrorModel()
        test_model.updt_lps(
            [["e", "e"], ["w", "w"], ["e", ""], ["a", "e"], ["e", "w"], ["", "b"], ["w", "w"], ["a", "a"]])
        self.assertEqual(test_model.p_i_g([["w", "w"], ["e", "e"]]), 0.6667)

    def test_align_words(self):
        self.assertEqual(align_words("wee", "wed"), [["w", "w"], ["e", "e"], ["e", "d"]])
        self.assertEqual(align_words("barber", "tarter"),
                         [["b", "t"], ["a", "a"], ["r", "r"], ["b", "t"], ["e", "e"], ["r", "r"]])

    def test_rec_list(self):
        test_model = ErrorModel()
        test_model.updt_lps(
            [["e", "e"], ["w", "w"], ["e", ""], ["a", "e"], ["e", "w"], ["", "b"], ["w", "w"], ["a", "a"]])
        self.assertEqual(test_model.rec_list("wee", 0.245, [["we", 0.321], ["web", 0.5], ["bee", 0.4]]),
                         [["wee", "wee", 0.245], ["we", "wee", 0.0713], ["web", "wee", 0.0],  ["bee", "wee", 0.0]])
