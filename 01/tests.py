import importlib
import unittest

a_fuel = getattr(importlib.import_module('01.a'), 'get_fuel')
b_fuel = getattr(importlib.import_module('01.b'), 'get_fuel')


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(a_fuel(12), 2)

    def test_two(self):
        self.assertEqual(a_fuel(14), 2)

    def test_three(self):
        self.assertEqual(a_fuel(1969), 654)

    def test_four(self):
        self.assertEqual(a_fuel(100756), 33583)


class TestBExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(b_fuel(14), 2)

    def test_two(self):
        self.assertEqual(b_fuel(1969), 966)

    def test_three(self):
        self.assertEqual(b_fuel(100756), 50346)
