from __future__ import print_function

import unittest
import numpy as np
import abstract_rendering.general as general


class IdTests(unittest.TestCase):
    def test(self):
        op = general.Id()

        aggs = np.zeros((4, 3))
        out = op.shade(aggs)
        self.assertIs(aggs, out)


class EmptyListTests(unittest.TestCase):
    def test(self):
        ls = general.EmptyList()
        self.assertIsNone(ls[0])
        self.assertIsNone(ls[-1])
        self.assertIsNone(ls[30])
        self.assertIsNone(ls[9048])
        self.assertIsNone(ls[100398384])
        self.assertIsNone(ls[3])
        self.assertIsNone(ls[490])


if __name__ == '__main__':
    unittest.main()
