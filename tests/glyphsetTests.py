import numpy as np
import unittest
import abstract_rendering.glyphset as glyphset


class UtilTests(unittest.TestCase):
    def _consts(self, f, condition, val):
        self.assertEqual(val, f(3), condition)
        self.assertEqual(val, f(4), condition)
        self.assertEqual(val, f(10), condition)
        self.assertEqual(val, f("Stuff"), "String (%s)" % condition)
        self.assertEqual(val, f(object()), "Object (%s)" % condition)
        self.assertEqual(val, f(None), "None (%s)" % condition)

    def test_const(self):
        f = glyphset.const(3)
        self._consts(f, "Number", 3)

        f = glyphset.const("two")
        self._consts(f, "String", "two")

        f = glyphset.const(None)
        self._consts(f, "None", None)

        o = object()
        f = glyphset.const(o)
        self._consts(f, "Object", o)

    def test_idx(self):
        f = glyphset.idx(2)
        self.assertEquals(2, f([0, 1, 2, 3, 4]))
        self.assertEquals(20, f([0, 10, 20, 30, 40]))
        self.assertIsNone(f([0, 1, None, 3, 4]), "None from list")
        self.assertEquals(3, f(xrange(1, 20)), "Function source")


class ShaperTests(unittest.TestCase):
    def test_Literals(self):
        f = glyphset.Literals(glyphset.ShapeCodes.LINE)
        l = [1, 2, 3, 4]
        self.assertIs(f(l), l)

        o = object()
        self.assertIs(f(o), o)
        self.assertIs(f(f), f)
        self.assertIs(f(0), 0)

    def test_ToRect(self):
        f = glyphset.ToRect(glyphset.idx(3), glyphset.idx(2), glyphset.idx(1), glyphset.idx(0))
        self.assertEquals(f([[1, 2, 3, 4, 5, 6]]), [[4, 3, 2, 1]], "Lists are indexable")
        self.assertEquals(f(["ABCDEF"]), [["D", "C", "B", "A"]], "Strings are indexable")
        self.assertEquals(f(["ABCDEF", "abcdef"]), [["D", "C", "B", "A"], ["d", "c", "b", "a"]], "multiple items")

        f = glyphset.ToRect(glyphset.idx(2), glyphset.idx(4), glyphset.idx(1), glyphset.idx(1))
        self.assertEquals(f([[1, 2, 3, 4, 5, 6]]), [[3, 5, 2, 2]])
        self.assertEquals(f(["ABCDEF"]), [["C", "E", "B", "B"]])

    def test_ToLine(self):
        f = glyphset.ToLine(glyphset.idx(3), glyphset.idx(2), glyphset.idx(1), glyphset.idx(0))
        self.assertEquals(f([[1, 2, 3, 4, 5, 6]]), [[4, 3, 2, 1]], "Lists are indexable")
        self.assertEquals(f(["ABCDEF"]), [["D", "C", "B", "A"]], "Strings are indexable")
        self.assertEquals(f(["ABCDEF", "abcdef"]), [["D", "C", "B", "A"], ["d", "c", "b", "a"]], "multiple items")

        f = glyphset.ToLine(glyphset.idx(2), glyphset.idx(4), glyphset.idx(1), glyphset.idx(1))
        self.assertEquals(f([[1, 2, 3, 4, 5, 6]]), [[3, 5, 2, 2]])
        self.assertEquals(f(["ABCDEF"]), [["C", "E", "B", "B"]])

    def test_ToPoint(self):
        f = glyphset.ToPoint(glyphset.idx(3), glyphset.idx(2))
        self.assertEquals(f([[1, 2, 3, 4, 5, 6]]), [[4, 3, 0, 0]], "Lists are indexable")
        self.assertEquals(f(["ABCDEF"]), [["D", "C", 0, 0]], "Strings are indexable")
        self.assertEquals(f(["ABCDEF", "abcdef"]), [["D", "C", 0, 0], ["d", "c", 0, 0]], "multiple items")

        f = glyphset.ToPoint(glyphset.idx(2), glyphset.idx(4))
        self.assertEquals(f([[1, 2, 3, 4, 5, 6]]), [[3, 5, 0, 0]])
        self.assertEquals(f(["ABCDEF"]), [["C", "E", 0, 0]])


class GlyphsetTests(unittest.TestCase):
    _glyphset = None

    def test_bounds(self):
        if not self._glyphset: return
        self.assertTrue(np.array_equal(self._glyphset.bounds(), self._bounds))

    def test_points(self):
        if not self._glyphset: return
        self.assertTrue(np.array_equal(self._glyphset.points(), self._points))

    def test_data(self):
        if not self._glyphset: return
        self.assertEquals(self._glyphset.data(), self._data)


class ArrayGlyphset(GlyphsetTests):
    def setUp(self):
        self._data = [1, 2, 3, 4, 5, 6]
        points = np.array([[0, 0], [1, 1], [.5, .5]])
        self._points = np.array([[0, 0, 0, 0], [1, 1, 0, 0], [.5, .5, 0, 0]])
        self._glyphset = glyphset.Glyphset(points, self._data, glyphset.ToPoint(glyphset.idx(0), glyphset.idx(1)))
        self._bounds = [0.0, 0.0, 1.0, 1.0]


class ColumnGlyphset(GlyphsetTests):
    def setUp(self):
        self._data = [1, 2, 3, 4, 5, 6]
        points = [[0, 1, .5], [0, 1, .5]]
        self._points = np.array([[0, 0, 0, 0], [1, 1, 0, 0], [.5, .5, 0, 0]])
        self._glyphset = glyphset.Glyphset(points, self._data, glyphset.ToPoint(glyphset.idx(0), glyphset.idx(1)), colMajor=True)
        self._bounds = [0.0, 0.0, 1.0, 1.0]

if __name__ == '__main__':
    unittest.main()
