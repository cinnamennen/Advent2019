import importlib
import unittest

a_soft_solve = getattr(importlib.import_module("07.a"), "soft_solve")
a_solve = getattr(importlib.import_module("07.a"), "solve")


# b_solve = getattr(importlib.import_module("07.b"), "solve")


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            43210,
            a_soft_solve(
                "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", [4, 3, 2, 1, 0]
            ),
        )

    def test_two(self):
        self.assertEqual(
            54321,
            a_soft_solve(
                "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
                [0, 1, 2, 3, 4],
            ),
        )

    def test_three(self):
        self.assertEqual(
            65210,
            a_soft_solve(
                "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
                [1, 0, 4, 3, 2],
            ),
        )


class TestASolutions(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            43210, a_solve("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0",),
        )

    def test_two(self):
        self.assertEqual(
            54321,
            a_solve(
                "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0",
            ),
        )

    def test_three(self):
        self.assertEqual(
            65210,
            a_solve(
                "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0",
            ),
        )
