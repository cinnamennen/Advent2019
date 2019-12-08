import importlib
import unittest

a_solve = getattr(importlib.import_module("08.a"), "solve")


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            1, a_solve(3, 2, "123456789012"),
        )
