import importlib
import unittest

a_soft_solve = getattr(importlib.import_module("07.b"), "soft_solve")

b_solve = getattr(importlib.import_module("07.b"), "solve")
# a_solve = getattr(importlib.import_module("07.a"), "solve")
a_solve = b_solve


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            1, a_solve("123456789012", 3, 2),
        )
