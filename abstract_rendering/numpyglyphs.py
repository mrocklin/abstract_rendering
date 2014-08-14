from __future__ import print_function, division
import numpy as np
from fast_project import _projectRects
import abstract_rendering.glyphset as glyphset
import abstract_rendering.core as ar


def is_identity_transform(vt):
    return vt == (0, 0, 1, 1)


class Glyphset(glyphset.Glyphset):
    # TODO: Default data is list of None (?)
    def __init__(self, points, data, vt=(0, 0, 1, 1)):
        self._table = points
        self.data = data
        self.vt = vt
        self.shaper = glyphset.ToPoint(glyphset.idx(0), glyphset.idx(1))

        if not is_identity_transform(vt):
            self.table = np.empty_like(points, dtype=np.int32)
            _projectRects(vt, points, self.table)
        else:
            self.table = points

    def data(self):
        return self.data

    def project(self, vt):
        """
        Project the points found in the glyphset with to the transform.

        vt -- convert canvas space to pixel space [tx,ty,sx,sy]
        returns a new glyphset with projected points and associated info values
        """
        nvt = (self.vt[0]+vt[0],
               self.vt[1]+vt[1],
               self.vt[2]*vt[2],
               self.vt[3]*vt[3])
        return Glyphset(self._table, nvt)

    def bounds(self):
        xmax = self.table[0].max()
        xmin = self.table[0].min()
        ymax = self.table[1].max()
        ymin = self.table[1].min()
        return (xmin, ymin, xmax-xmin, ymax-ymin)


class PointCount(ar.Aggregator):
    def aggregate(self, glyphset, info, screen):
        sparse = glyphset.table
        dense = np.histogram2d(sparse[:, 0], sparse[:, 1], screen)
        return dense[0]

    def rollup(self, *vals):
        return reduce(lambda x, y: x+y,  vals)


class PointCountCategories(ar.Aggregator):
    def aggregate(self, glyphset, info, screen):
        points = glyphset.table
        dims = screen + np.unique(glyphset.data()),
        data = np.hstac([points, map(list, glyphset.data())])
        dense = np.histogramdd(data, dims)
        return dense[0]

    def rollup(self, *vals):
        """NOTE: Assumes co-registration of categories..."""
        return reduce(lambda x, y: x+y,  vals)


def load_csv(filename, skip, xc, yc, vc):
    """Turn a csv file into a glyphset.

    This is a fairly naive regulary-expression based parser
    (it doesn't handle quotes, blank lines or much else).
    It is useful for getting simple datasets into the system.
    """
    import re
    source = open(filename, 'r')
    glyphs = []
    data = []

    for i in range(0, skip):
        source.readline()

    for line in source:
        line = re.split("\s*,\s*", line)
        x = float(line[xc].strip())
        y = float(line[yc].strip())
        v = float(line[vc].strip()) if vc >= 0 else 1
        g = [x, y, 0, 0]
        glyphs.append(g)
        data.append(v)

    source.close()
    return Glyphset(np.array(glyphs), np.array(data))


def load_hdf(filename, node, xc, yc, vc=-1):
    "Load a node from an HDF file."
    import pandas as pd
    table = pd.read_hdf(filename, node)
    points = table[[xc, yc]]
    data = table[vc] if vc >= 0 else None

    # Is this copy needed?  After all, projection makes a copy too...
    #    maybe the input just needs to be CLOSE to a numpy array
    return Glyphset(np.array(points), np.array(data))
