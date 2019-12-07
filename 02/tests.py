import importlib
import unittest

a_solve = getattr(importlib.import_module("02.a"), "soft_solve")


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertListEqual(a_solve("1,0,0,0,99"), [2, 0, 0, 0, 99])

    def test_two(self):
        self.assertListEqual(a_solve("2,3,0,3,99"), [2, 3, 0, 6, 99])

    def test_three(self):
        self.assertListEqual(a_solve("2,4,4,5,99,0"), [2, 4, 4, 5, 99, 9801])

    def test_four(self):
        self.assertListEqual(
            a_solve("1,1,1,4,99,5,6,0,99"), [30, 1, 1, 4, 2, 5, 6, 0, 99]
        )
