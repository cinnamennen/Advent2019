import importlib
import unittest

a_solve = getattr(importlib.import_module('04.a'), 'test')
b_solve = getattr(importlib.import_module('04.b'), 'test')


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertTrue(a_solve('111111'))

    def test_two(self):
        self.assertFalse(a_solve('223450'))

    def test_three(self):
        self.assertFalse(a_solve('123789'))


class TestBExamples(unittest.TestCase):
    def test_one(self):
        self.assertTrue(b_solve('112233'))

    def test_two(self):
        self.assertFalse(b_solve('123444'))

    def test_three(self):
        self.assertTrue(b_solve('111122'))
