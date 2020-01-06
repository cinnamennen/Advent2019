import importlib
import unittest

from cinnamon_tools.point import Point

a_solve = getattr(importlib.import_module("15.a"), "solve")
b_solve = getattr(importlib.import_module("15.b"), "solve")


class Test15Examples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            31,
            a_solve(
                data=(
                    "10 ORE => 10 A\n"
                    "1 ORE => 1 B\n"
                    "7 A, 1 B => 1 C\n"
                    "7 A, 1 C => 1 D\n"
                    "7 A, 1 D => 1 E\n"
                    "7 A, 1 E => 1 FUEL"
                )
            ),
        )
