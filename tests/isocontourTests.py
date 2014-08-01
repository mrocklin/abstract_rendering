from __future__ import print_function
import unittest
import numpy as np
import abstract_rendering.isocontour as iso


class CountTests(unittest.TestCase):
    pyramid2 = np.array(
            [[0, 0, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]])

    pyramid4 = np.array(
            [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 2, 2, 2, 2, 1, 0],
             [0, 1, 2, 3, 3, 3, 1, 0],
             [0, 1, 2, 3, 3, 3, 1, 0],
             [0, 1, 2, 3, 3, 3, 1, 0],
             [0, 1, 2, 2, 2, 2, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]])

    def test_nlevels(self):
        self.assertListEqual(iso.Contour.nlevels(self.pyramid2, 2).tolist(), [0, 1])
        self.assertListEqual(iso.Contour.nlevels(self.pyramid2, 3).tolist(), [0, .5, 1])
        self.assertListEqual(iso.Contour.nlevels(self.pyramid4, 2).tolist(), [0, 3])
        self.assertListEqual(iso.Contour.nlevels(self.pyramid4, 4).tolist(), [0, 1, 2, 3])

    def test_fuse2(self):
        c = iso.Contour(levels=2)
        levels = c.fuse(self.pyramid2)

        expected = [[(1.0, 0.0),
                     (2.0, 0.0),
                     (3.0, 1.0),
                     (3.0, 2.0),
                     (2.0, 3.0),
                     (1.0, 3.0),
                     (0.0, 2.0),
                     (0.0, 1.0),
                     (1.0, 0.0)]]
        self.assertListEqual(levels, expected)


if __name__ == '__main__':
    unittest.main()
