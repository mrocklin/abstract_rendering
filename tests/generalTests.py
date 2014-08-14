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
    def test_without_length(self):
        ls = general.EmptyList()
        self.assertIsNone(ls[0])
        self.assertIsNone(ls[-1])
        self.assertIsNone(ls[30])
        self.assertIsNone(ls[9048])
        self.assertIsNone(ls[100398384])
        self.assertIsNone(ls[3])
        self.assertIsNone(ls[490])

    def test_with_length(self):
        ls = general.EmptyList(7)
        self.assertIsNone(ls[0])
        self.assertIsNone(ls[1])
        self.assertIsNone(ls[2])
        self.assertIsNone(ls[3])
        self.assertIsNone(ls[4])
        self.assertIsNone(ls[5])
        self.assertIsNone(ls[6])

        self.assertRaises(IndexError, ls.__getitem__, -1)
        self.assertRaises(IndexError, ls.__getitem__, 8)

if __name__ == '__main__':
    unittest.main()
