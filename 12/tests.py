import importlib
import unittest

from cinnamon_tools.point import Point

a_solve = getattr(importlib.import_module("12.a"), "solve")
a_moon = getattr(importlib.import_module("12.a"), "Moon")


class TestSimulation(unittest.TestCase):
    def test_gravity_a(self):
        ganymede = a_moon(Point(3, 0, 0))
        callisto = a_moon(Point(5, 0, 0))

        ganymede.apply_gravity(callisto)

        with self.subTest("Ganymede correct"):
            self.assertEqual(Point(1, 0, 0), ganymede.velocity)
        with self.subTest("Callisto correct"):
            self.assertEqual(Point(-1, 0, 0), callisto.velocity)

    def test_gravity_b(self):
        ganymede = a_moon(Point(3, 0, 0))
        callisto = a_moon(Point(5, 0, 0))

        callisto.apply_gravity(ganymede)

        with self.subTest("Ganymede correct"):
            self.assertEqual(Point(1, 0, 0), ganymede.velocity)
        with self.subTest("Callisto correct"):
            self.assertEqual(Point(-1, 0, 0), callisto.velocity)

    def test_velocity(self):
        europa = a_moon(Point(1, 2, 3), Point(-2, 0, 3))
        europa.apply_velocity()
        self.assertEqual(Point(-1, 2, 6), europa.position)


class TestCalculations(unittest.TestCase):
    def test_a(self):
        m = a_moon(Point(2, 1, 3), Point(3, 2, 1))
        with self.subTest('Potential'):
            self.assertEqual(6, m.potential_energy)
        with self.subTest('Kinetic'):
            self.assertEqual(6, m.kinetic_energy)
        with self.subTest('Total'):
            self.assertEqual(36, m.total_energy)


class Test12Examples(unittest.TestCase):
    def test_one(self):
        self.assertEqual(
            179,
            a_solve(
                data=[
                    "<x=-1, y=0, z=2>",
                    "<x=2, y=-10, z=-7>",
                    "<x=4, y=-8, z=8>",
                    "<x=3, y=5, z=-1>",
                ],
                steps=10,
            ),
        )

    def test_two(self):
        self.assertEqual(
            1940,
            a_solve(
                data=[
                    '<x=-8, y=-10, z=0>',
                    '<x=5, y=5, z=10>',
                    '<x=2, y=-7, z=3>',
                    '<x=9, y=-8, z=-3>',
                ],
                steps=100,
            ),
        )
