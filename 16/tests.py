import importlib
import unittest

from cinnamon_tools.point import Point

a_solve = getattr(importlib.import_module("16.a"), "solve")
# b_solve = getattr(importlib.import_module("16.b"), "solve")
get_pattern = getattr(importlib.import_module("16.a"), "get_pattern")


class TestPattern(unittest.TestCase):
    def test_one(self):
        self.assertEqual([0, 1, 0, -1], get_pattern(1))

    def test_two(self):
        self.assertEqual([0, 0, 1, 1, 0, 0, -1, -1], get_pattern(2))

    def test_three(self):
        self.assertEqual([0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1], get_pattern(3))

    def test_four(self):
        self.assertEqual(
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, -1, -1, -1, -1], get_pattern(4)
        )


class Test16Examples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            "24176176", a_solve(data="80871224585914546619083218645595\n"),
        )

    def test_two(self):
        self.assertEqual(
            "73745418", a_solve(data="19617804207202209144916044189917\n"),
        )

    def test_three(self):
        self.assertEqual(
            "52432133", a_solve(data="69317163492948606335995924319873\n"),
        )
