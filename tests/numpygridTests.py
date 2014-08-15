from __future__ import print_function

import unittest
import numpy as np
import abstract_rendering.numpyglyphs as npg


class SpreadTests(unittest.TestCase):
    def run_spread(self, spread, in_vals, expected):
        op = npg.Spread(factor=spread)
        out = op.shade(in_vals)

        self.assertTrue(np.array_equal(out, expected),
                        'incorrect value spreading\ni %s' % str(out))

    def test_spread_oneseed(self):
        a = np.asarray([[0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])

        ex = np.asarray([[1, 1, 1, 0],
                         [1, 1, 1, 0],
                         [1, 1, 1, 0],
                         [0, 0, 0, 0]])
        self.run_spread(1, a, ex)

    def test_spread_twoseeds(self):
        a = np.asarray([[0, 0, 0, 0],
                        [0, 1, 1, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])

        ex = np.asarray([[1, 2, 2, 1],
                         [1, 2, 2, 1],
                         [1, 2, 2, 1],
                         [0, 0, 0, 0]])
        self.run_spread(1, a, ex)

    def test_spread_two(self):
        a = np.asarray([[0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])

        ex = np.asarray([[1, 1, 1, 1],
                         [1, 1, 1, 1],
                         [1, 1, 1, 1],
                         [1, 1, 1, 1]])
        self.run_spread(2, a, ex)

    def test_spread_zero(self):
        a = np.asarray([[0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])

        ex = np.asarray([[0, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
        self.run_spread(0, a, ex)


    def test_spread_cats(self):
        a = np.asarray([[[0, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]],
                        [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 0]]])
        
        b = np.asarray([[[1, 1, 1, 0],
                         [1, 1, 1, 0],
                         [1, 1, 1, 0],
                         [0, 0, 0, 0]],
                        [[0, 0, 0, 0],
                         [0, 1, 1, 1],
                         [0, 1, 1, 1],
                         [0, 1, 1, 1]]])
        self.run_spread(1, a, b)



if __name__ == '__main__':
    unittest.main()
