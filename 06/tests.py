import importlib
import unittest

a_solve = getattr(importlib.import_module('06.a'), 'solve')


b_solve = getattr(importlib.import_module('06.b'), 'solve')


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(a_solve(["COM)B",
                                  "B)C",
                                  "C)D",
                                  "D)E",
                                  "E)F",
                                  "B)G",
                                  "G)H",
                                  "D)I",
                                  "E)J",
                                  "J)K",
                                  "K)L",
                                  ]), 42)


class TestBExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(b_solve(["COM)B",
                                  "B)C",
                                  "C)D",
                                  "D)E",
                                  "E)F",
                                  "B)G",
                                  "G)H",
                                  "D)I",
                                  "E)J",
                                  "J)K",
                                  "K)L",
                                  "K)YOU",
                                  "I)SAN",
                                  ]), 4)
