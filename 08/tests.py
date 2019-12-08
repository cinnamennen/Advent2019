import importlib
import unittest

a_solve = getattr(importlib.import_module("08.a"), "solve")
b_solve = getattr(importlib.import_module("08.b"), "soft_solve")
b_r = getattr(importlib.import_module("08.b"), "pre_raster")
b_l = getattr(importlib.import_module("08.b"), "get_layers")


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            1, a_solve(3, 2, "123456789012"),
        )


class TestBExamples(unittest.TestCase):
    def test_one(self):
        self.assertListEqual(
            [[0, 2, 2, 2], [1, 1, 2, 2], [2, 2, 1, 2], [0, 0, 0, 0]],
            b_l(2, 2, "0222112222120000"),
        )

    def test_two(self):
        self.assertListEqual(
            [[0, 1, 2, 0], [2, 1, 2, 0], [2, 2, 1, 0], [2, 2, 2, 0]],
            b_r(2, 2, "0222112222120000"),
        )

    def test_three(self):
        self.assertListEqual(
            [0, 1, 1, 0], b_solve(2, 2, "0222112222120000"),
        )
