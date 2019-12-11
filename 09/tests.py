import importlib
import unittest

a_solve = getattr(importlib.import_module("09.a"), "solve")


class TestAExamples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99".replace(
                ",", ""
            ),
            a_solve("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"),
        )

    def test_two(self):

        output = a_solve("1102,34915192,34915192,7,4,7,99,0")
        with self.subTest("output makes sense"):
            self.assertEqual("1219070632396864", output)
        with self.subTest("length is correct"):
            self.assertEqual(16, len(output))

    def test_three(self):
        self.assertEqual("1125899906842624", a_solve("104,1125899906842624,99"))
