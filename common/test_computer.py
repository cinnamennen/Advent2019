import unittest

from common.computer import computer_from_string


def a_solve(data=None, data_in=None):
    if data_in is None:
        data_in = []
    c = computer_from_string(data)
    while data_in:
        c.data_in.put(data_in.pop(0))
    return c.run(), c


class Test2A(unittest.TestCase):
    def test_example_one(self):
        self.assertListEqual([2, 0, 0, 0, 99], a_solve("1,0,0,0,99")[1].memory)

    def test_example_two(self):
        self.assertListEqual([2, 3, 0, 6, 99], a_solve("2,3,0,3,99")[1].memory)

    def test_example_three(self):
        self.assertListEqual([2, 4, 4, 5, 99, 9801], a_solve("2,4,4,5,99,0")[1].memory)

    def test_example_four(self):
        self.assertListEqual(
            [30, 1, 1, 4, 2, 5, 6, 0, 99], a_solve("1,1,1,4,99,5,6,0,99")[1].memory
        )

    def test_final(self):
        c = computer_from_string(
            "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,9,23,1,23,9,27,1,10,27,31,1,13,31,35,1,35,10,39,2,39,"
            "9,43,1,43,13,47,1,5,47,51,1,6,51,55,1,13,55,59,1,59,6,63,1,63,10,67,2,67,6,71,1,71,5,75,2,75,10,79,"
            "1,79,6,83,1,83,5,87,1,87,6,91,1,91,13,95,1,95,6,99,2,99,10,103,1,103,6,107,2,6,107,111,1,13,111,115,"
            "2,115,10,119,1,119,5,123,2,10,123,127,2,127,9,131,1,5,131,135,2,10,135,139,2,139,9,143,1,143,2,147,"
            "1,5,147,0,99,2,0,14,0",
        )
        c.memory[1] = 76
        c.memory[2] = 3
        c.run()
        self.assertEqual(
            19690720, c.memory[0],
        )


class Test5AExamples(unittest.TestCase):
    def test_one(self):
        self.assertListEqual([1002, 4, 3, 4, 99], a_solve("1002,4,3,4,33")[1].memory)

    def test_two(self):
        self.assertEqual("1", a_solve("3,0,4,0,99", [1])[0])


class Test5BExamples(unittest.TestCase):
    def test_one(self):
        program = "3,9,8,9,10,9,4,9,99,-1,8"
        self.assertEqual("1", a_solve(program, [8])[0])
        self.assertEqual("0", a_solve(program, [5])[0])
        self.assertEqual("0", a_solve(program, [18])[0])

    def test_two(self):
        program = "3,9,7,9,10,9,4,9,99,-1,8"
        self.assertEqual("0", a_solve(program, [8])[0])
        self.assertEqual("1", a_solve(program, [5])[0])
        self.assertEqual("0", a_solve(program, [18])[0])

    def test_three(self):
        program = "3,3,1108,-1,8,3,4,3,99"
        self.assertEqual("1", a_solve(program, [8])[0])
        self.assertEqual("0", a_solve(program, [5])[0])
        self.assertEqual("0", a_solve(program, [18])[0])

    def test_four(self):
        program = "3,3,1107,-1,8,3,4,3,99"
        self.assertEqual("0", a_solve(program, [8])[0])
        self.assertEqual("1", a_solve(program, [5])[0])
        self.assertEqual("0", a_solve(program, [18])[0])

    def test_five(self):
        program = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
        for i in range(-3, 4):
            with self.subTest(i=i):
                output = a_solve(program, [i])
                expected = "0" if i == 0 else "1"
                self.assertEqual(expected, output[0])

    def test_six(self):
        program = "3,3,1105,-1,9,1101,0,0,12,4,12,99,1"
        for i in range(-3, 4):
            with self.subTest(i=i):
                output = a_solve(program, [i])
                expected = "0" if i == 0 else "1"
                self.assertEqual(expected, output[0])

    def test_seven(self):
        program = (
            "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
            "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
            "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        )

        for i in range(-1, 8):
            with self.subTest("less", i=i):
                self.assertEqual("999", a_solve(program, [i])[0])
        with self.subTest("equal", i=8):
            self.assertEqual("1000", a_solve(program, [8])[0])
        for i in range(9, 12):
            with self.subTest("greater", i=i):
                self.assertEqual("1001", a_solve(program, [i])[0])


class Test9AExamples(unittest.TestCase):
    def test_one(self):
        program = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
        self.assertEqual(
            program.replace(",", "\n"),
            a_solve(program, )[0],
        )

    def test_two(self):
        output = a_solve("1102,34915192,34915192,7,4,7,99,0", )[0]
        with self.subTest("output makes sense"):
            self.assertEqual(
                "1219070632396864", output,
            )
        with self.subTest("length is correct"):
            self.assertEqual(
                16, len(output),
            )

    def test_three(self):
        self.assertEqual(
            "1125899906842624", a_solve("104,1125899906842624,99", )[0],
        )
