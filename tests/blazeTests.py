from __future__ import print_function

import unittest
import numpy as np
import abstract_rendering.blazeglyphs as ar_blz
import abstract_rendering.glyphset as glyphset
import abstract_rendering.core as core
import abstract_rendering.util as util

class GlyphsetTests(unittest.TestCase):
    def setUp(self):
        self._glyphset = ar_blz.load_csv("../data/circlepoints.csv", "x", "y", "series",
                                         schema="{r:float32, theta:float32, x:float32, y:float32, series:int32}")

    def test_bounds(self):
        expected = (-0.9868608117103577, -0.9927806854248047, 1.9690493941307068, 1.9707229733467102)
        self.assertEquals(self._glyphset.bounds(), expected)

    def test_project(self):
        identity = self._glyphset.project([0, 0, 1, 1])
        self.assertEquals(self._glyphset.bounds(), identity.bounds())

        translate = self._glyphset.project([10, 10, 1, 1])
        expected = tuple(sum(t) for t in zip(self._glyphset.bounds(), (10, 10, 0, 0))) 
        self.assertEquals(expected, translate.bounds())

        translate = self._glyphset.project([0, 0, 10, 10])
        expected = tuple(a*b for (a,b) in zip(self._glyphset.bounds(), (10, 10, 10, 10))) 
        self.assertEquals(expected, translate.bounds())

        compound = self._glyphset.project([2, 2, 5, 5])
        expected = self._glyphset.bounds()
        expected = tuple(a*b for (a,b) in zip(expected, (5, 5, 5, 5))) 
        expected = tuple(a+b for (a,b) in zip(expected, (2, 2, 0, 0))) 
        self.assertEquals(expected, compound.bounds())

        sequential = self._glyphset.project([2, 2, 2, 2])
        sequential = sequential.project([3, 3, 3, 3])
        expected = self._glyphset.bounds()
        expected = tuple(a*b for (a,b) in zip(expected, (6, 6, 6, 6))) 
        expected = tuple(a+b for (a,b) in zip(expected, (5, 5, 0, 0))) 
        self.assertEquals(expected, sequential.bounds())
    
    def test_matches(self):
        screen = (800,800)
        ref = glyphset.load_csv("../data/circlepoints.csv", 1, 2, 3, 4,.1,.1, glyphset.ShapeCodes.POINT)
        self.assertEquals(roundAll(ref.bounds()), roundAll(self._glyphset.bounds()))


        refzoom = util.zoom_fit(screen, ref.bounds()) 
        reszoom = util.zoom_fit(screen, self._glyphset.bounds())
        self.assertEquals(roundAll(refzoom, 4), roundAll(reszoom, 4))


def roundAll(ls, p=7):
    return map(lambda n: round(n, p), ls)

if __name__ == '__main__':
    unittest.main()
