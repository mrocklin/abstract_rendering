from __future__ import print_function

import unittest
import abstract_rendering.core as core


class ColorTest(unittest.TestCase):
    def _test(self, r, g, b, a):
        c = core.Color(r, g, b, a)
        self.assertEqual(core.Color(r, g, b, a), c)
        self.assertEqual(c.asarray().tolist(),  [r, g, b, a])

    def test1(self): self._test(0, 0, 0, 0)
    def test2(self): self._test(10, 30, 40, 20)
    def test3(self): self._test(255, 255, 255, 255)

    def test_RedError(self):
        self.assertRaises(ValueError, core.Color, 256, 0, 0, 0)
        self.assertRaises(ValueError, core.Color, -1, 0, 0, 0)

    def test_GreenError(self):
        self.assertRaises(ValueError, core.Color, 0, 256, 0, 0)
        self.assertRaises(ValueError, core.Color, 0, -1, 0, 0)

    def test_BlueError(self):
        self.assertRaises(ValueError, core.Color, 0, 0, 256, 0)
        self.assertRaises(ValueError, core.Color, 0, 0, -1, 0)

    def test_AlphaError(self):
        self.assertRaises(ValueError, core.Color, 0, 0, 0, 256)
        self.assertRaises(ValueError, core.Color, 0, 0, 0, -1)


class ZoomFitTest(unittest.TestCase):
    def test_scale(self):
        self.assertEqual(core.zoom_fit((10, 10), (0, 0, 10, 10)),
                         [0., 0., 1., 1.])

        self.assertEqual(core.zoom_fit((10, 10), (0, 0, 20, 20)),
                         [0., 0., .5, .5])

        self.assertEqual(core.zoom_fit((10, 10), (0, 0, 5, 5)),
                         [0., 0., 2., 2.])

        self.assertEqual(core.zoom_fit((10, 10), (0, 0, 10, 20)),
                         [0., 0., .5, .5])

        self.assertEqual(core.zoom_fit((10, 10), (0, 0, 10, 20), False),
                         [0., 0., 1., .5])

    def test_pan(self):
        self.assertEqual(core.zoom_fit((10, 10), (0, 0, 10, 10)),
                         [0., 0., 1., 1.])

        self.assertEqual(core.zoom_fit((10, 10), (5, 5, 10, 10)),
                         [-5., -5., 1., 1.])

        self.assertEqual(core.zoom_fit((10, 10), (-4, -7, 10, 10)),
                         [4., 7., 1., 1.])

    def test_pan_scale(self):
        self.assertEqual(core.zoom_fit((10, 10), (0, 0, 20, 20)),
                         [0., 0., .5, .5])

        self.assertEqual(core.zoom_fit((10, 10), (5, 5, 20, 20)),
                         [-2.5, -2.5, .5, .5])

        self.assertEqual(core.zoom_fit((10, 10), (-4, -7, 20, 20)),
                         [2., 3.5, .5, .5])


if __name__ == '__main__':
    unittest.main()
