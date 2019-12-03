import importlib
import unittest

a_solve = getattr(importlib.import_module('03.a'), 'solve')
b_solve = getattr(importlib.import_module('03.b'), 'solve')


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(a_solve(['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']), 159)

    def test_two(self):
        self.assertEqual(
            a_solve(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']), 135)

    def test_three(self):
        self.assertEqual(a_solve(['R8,U5,L5,D3', 'U7,R6,D4,L4']), 6)


class TestBExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(b_solve(['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']), 610)

    def test_two(self):
        self.assertEqual(
            b_solve(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']), 410)

    def test_three(self):
        self.assertEqual(b_solve(['R8,U5,L5,D3', 'U7,R6,D4,L4']), 30)
