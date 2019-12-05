import importlib
import unittest

a_solve = getattr(importlib.import_module('05.a'), 'soft_solve')

b_solve = getattr(importlib.import_module('05.b'), 'soft_solve')


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertListEqual(a_solve('1002,4,3,4,33'), [1002, 4, 3, 4, 99])

    def test_two(self):
        self.assertListEqual(a_solve('3,0,4,0,99'), [1, 0, 4, 0, 99])


class TestBExamples(unittest.TestCase):
    def test_one(self):
        program = '3,9,8,9,10,9,4,9,99,-1,8'
        self.assertEqual(b_solve(program, 8), '1')
        self.assertEqual(b_solve(program, 5), '0')
        self.assertEqual(b_solve(program, 18), '0')

    def test_two(self):
        program = '3,9,7,9,10,9,4,9,99,-1,8'
        self.assertEqual(b_solve(program, 8), '0')
        self.assertEqual(b_solve(program, 5), '1')
        self.assertEqual(b_solve(program, 18), '0')

    def test_three(self):
        program = '3,3,1108,-1,8,3,4,3,99'
        self.assertEqual(b_solve(program, 8), '1')
        self.assertEqual(b_solve(program, 5), '0')
        self.assertEqual(b_solve(program, 18), '0')

    def test_four(self):
        program = '3,3,1107,-1,8,3,4,3,99'
        self.assertEqual(b_solve(program, 8), '0')
        self.assertEqual(b_solve(program, 5), '1')
        self.assertEqual(b_solve(program, 18), '0')

    def test_five(self):
        program = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
        for i in range(-3, 4):
            with self.subTest(i=i):
                output = b_solve(program, i)
                expected = '0' if i == 0 else '1'
                self.assertEqual(output, expected)

    def test_six(self):
        program = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
        for i in range(-3, 4):
            with self.subTest(i=i):
                output = b_solve(program, i)
                expected = '0' if i == 0 else '1'
                self.assertEqual(output, expected)

    def test_seven(self):
        program = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,' \
                  '1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,' \
                  '999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'

        for i in range(-1, 8):
            with self.subTest('less', i=i):
                self.assertEqual(b_solve(program, i), '999')
        with self.subTest('equal', i=8):
            self.assertEqual(b_solve(program, 8), '1000')
        for i in range(9, 12):
            with self.subTest('greater', i=i):
                self.assertEqual(b_solve(program, i), '1001')

    def test_eight(self):
        program = '1002,4,3,4,33'
        self.assertEqual(b_solve(program, 1), '')

    def test_nine(self):
        program = '3,0,4,0,99'
        self.assertEqual(b_solve(program, 1), '1')
        self.assertEqual(b_solve(program, -1), '-1')
        self.assertEqual(b_solve(program, 100), '100')
