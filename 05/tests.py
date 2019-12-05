import importlib
import unittest

a_solve = getattr(importlib.import_module('05.a'), 'soft_solve')


# b_solve = getattr(importlib.import_module('05.b'), 'test')


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertListEqual(a_solve('1002,4,3,4,33'), [1002, 4, 3, 4, 99])

    def test_two(self):
        self.assertListEqual(a_solve('3,0,4,0,99'), [1, 0, 4, 0, 99])
