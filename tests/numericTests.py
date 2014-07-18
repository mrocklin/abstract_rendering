import unittest
import numpy as np
import abstract_rendering.numeric as numeric
from abstract_rendering.glyphset import ShapeCodes


class Count(unittest.TestCase):
    def test_allocate(self):
        op = numeric.Count()
        init = op.allocate(10, 10, None, None)  # Does not depend on glyphset or info
        self.assertEquals(init.shape, (10, 10))
        self.assertTrue(np.array_equal(init, np.zeros((10, 10))))

    def test_combine(self):
        op = numeric.Count()
        glyph = [0, 0, 1, 1]

        existing = np.zeros((1, 1))
        op.combine(existing, glyph, ShapeCodes.POINT, 10)
        self.assertTrue(np.array_equal(existing, np.ones((1, 1))))

        existing = np.zeros((1, 1))
        op.combine(existing, glyph, ShapeCodes.POINT, 20)
        self.assertTrue(np.array_equal(existing, np.ones((1, 1))),
                        "Not input value invariant")

        existing = np.ones((1, 1))
        op.combine(existing, glyph, ShapeCodes.POINT, 20)
        self.assertTrue(np.array_equal(existing, np.array([[2]])),
                        "Count up from non-zero")



        glyph = [1, 2, 2, 3]
        existing = np.ones((3,1))
        expected = np.array([[1, 1, 1, 1],
                             [1, 1, 1, 1],
                             [1, 2, 1, 1]])
        op.combine(existing, glyph, ShapeCodes.POINT, 3)


        glyph = [5, 5, 6, 6]
        existing = np.ones((10, 10))
        expected = np.ones((10, 10))
        expected[5, 5] = 2
        op.combine(existing, glyph, ShapeCodes.POINT, 20)
        self.assertTrue(np.array_equal(existing, expected),
                        "Setting in the middle")

    def test_rollup(self):
        op = numeric.Count()
        ones = np.ones((5, 5))
        twos = np.empty((5, 5))
        twos.fill(2)

        result = op.rollup(ones, ones)
        self.assertTrue(np.array_equal(result, twos))


class Sum(unittest.TestCase):
    def test_allocate(self):
        op = numeric.Sum()
        init = op.allocate(10, 10, None, None)  # Does not depend on glyphset or info
        self.assertEquals(init.shape, (10, 10))
        self.assertTrue(np.array_equal(init, np.zeros((10, 10))))

    def test_combine(self):
        op = numeric.Sum()
        glyph = [0, 0, 1, 1]

        existing = np.ones((1, 1))
        expected = np.empty((1, 1))
        expected.fill(11)

        op.combine(existing, glyph, ShapeCodes.POINT, 10)
        self.assertTrue(np.array_equal(existing, expected))

        existing = np.ones((1, 1))
        expected = np.empty((1, 1))
        expected.fill(21)
        op.combine(existing, glyph, ShapeCodes.POINT, 20)
        self.assertTrue(np.array_equal(existing, expected))


        glyph = [1, 2, 2, 3]
        existing = np.ones((3,1))
        expected = np.array([[1, 1, 1, 1],
                             [1, 1, 1, 1],
                             [1, 4, 1, 1]])
        op.combine(existing, glyph, ShapeCodes.POINT, 3)

        glyph = [5, 5, 6, 6]
        existing = np.ones((10, 10))
        expected = np.ones((10, 10))
        expected[5, 5] = 21
        op.combine(existing, glyph, ShapeCodes.POINT, 20)
        self.assertTrue(np.array_equal(existing, expected),
                        "Setting in the middle")

    def test_rollup(self):
        op = numeric.Count()
        ones = np.ones((5, 5))
        twos = np.empty((5, 5))
        twos.fill(2)

        result = op.rollup(ones, ones)
        self.assertTrue(np.array_equal(result, twos))


class FlattenCategories(unittest.TestCase):
    pass


class Floor(unittest.TestCase):
    def test(self):
        op = numeric.Floor()
        a = np.array([[1.1, 1.5, 1.9],
                      [2.3, 0, 0.1]])

        expected = np.array([[1,   1,  1],
                             [2,   0,  0]], dtype=float)

        out = op.shade(a)
        self.assertTrue(np.array_equal(out, expected),
                        "Unequal:\n %s \n = \n %s" % (out, expected))


class Interpolate(unittest.TestCase):
    pass


class Power(unittest.TestCase):
    def test(self):
        op = numeric.Power(2)
        out = op.shade([0, 0, 0])
        self.assertTrue(np.array_equal(out, [0, 0, 0]))

        a = np.array([[1, 1, 1],
                      [2, 2, 2],
                      [5, 5, 5]])

        expected = np.array([[1,   1,  1],
                             [4,   4,  4],
                             [25, 25, 25]], dtype=float)

        out = op.shade(a)
        self.assertTrue(np.array_equal(out, expected),
                        "Unequal:\n %s \n = \n %s" % (out, expected))


class Cuberoot(unittest.TestCase):
    def test(self):
        op = numeric.Cuberoot()
        out = op.shade([1, 1, 1])
        self.assertTrue(np.array_equal(out, [1, 1, 1]))

        a = np.array([[27],
                      [64],
                      [125]])

        # Calculates in-place because of floating point round-off
        expected = np.array([[pow(27, 1/3.0)],
                             [pow(64, 1/3.0)],
                             [pow(125, 1/3.0)]], dtype=float)

        out = op.shade(a)
        self.assertTrue(np.array_equal(out, expected),
                        "Unequal:\n %s \n = \n %s" % (out, expected))


class Sqrt(unittest.TestCase):
    def test(self):
        op = numeric.Sqrt()
        out = op.shade([1, 1, 1])
        self.assertTrue(np.array_equal(out, [1, 1, 1]))

        a = np.array([[4,   4,  4],
                      [9,   9,  9],
                      [25, 25, 25]])

        expected = np.array([[2, 2, 2],
                             [3, 3, 3],
                             [5, 5, 5]], dtype=float)

        out = op.shade(a)
        self.assertTrue(np.array_equal(out, expected),
                        "Unequal:\n %s \n = \n %s" % (out, expected))


class AbsSegment(unittest.TestCase):
    pass


class InterpolateColors(unittest.TestCase):
    pass


class Spread(unittest.TestCase):
    def run_spread(self, spread, in_vals, expected):
        spread = numeric.Spread(spread)
        out = spread.shade(in_vals)

        self.assertTrue(np.array_equal(out, expected), 'incorrect value spreading')

    def test_spread_oneseed(self):
        a = np.asarray([[0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])

        ex = np.asarray([[0, 0, 0, 0],
                         [0, 1, 1, 0],
                         [0, 1, 1, 0],
                         [0, 0, 0, 0]])
        self.run_spread(2, a, ex)

    def test_spread_twoseeds(self):
        a = np.asarray([[0, 0, 0, 0],
                        [0, 1, 1, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])

        ex = np.asarray([[0, 0, 0, 0],
                         [0, 1, 2, 1],
                         [0, 1, 2, 1],
                         [0, 0, 0, 0]])
        self.run_spread(2, a, ex)

    def test_spread_three(self):
        a = np.asarray([[0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])

        ex = np.asarray([[1, 1, 1, 0],
                         [1, 1, 1, 0],
                         [1, 1, 1, 0],
                         [0, 0, 0, 0]])
        self.run_spread(3, a, ex)

    def spread_zero(self):
        a = np.asarray([[0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])

        ex = np.asarray([[0, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
        self.run_spread(0, a, ex)


if __name__ == '__main__':
    unittest.main()
