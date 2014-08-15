from __future__ import print_function, division
import numpy as np
from scipy.ndimage.filters import convolve
from fast_project import _projectRects
import abstract_rendering.glyphset as glyphset
import abstract_rendering.core as ar


class Glyphset(glyphset.Glyphset):
    # TODO: Default data is list of None (?)
    def __init__(self, points, data, vt=(0, 0, 1, 1)):
        self._table = points
        self._data = data
        self.vt = vt
        self.shaper = glyphset.ToPoint(glyphset.idx(0), glyphset.idx(1))

        if not is_identity_transform(vt):
            self.table = np.empty_like(points, dtype=np.int32)
            _projectRects(vt, points, self.table)
        else:
            self.table = points

    def data(self):
        return self._data

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
        return Glyphset(self._table, self._data, nvt)

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


class Spread(ar.CellShader):
    """
    Spreads the values out in a regular pattern.
    Spreads categories inside their category plane (not between planes).
    
    * factor : How far in each direction to spread
    """
    def __init__(self, factor=1):
        self.factor = factor

    def shade(self, grid):
        kShape = (self.factor*2+1, self.factor*2+1) + grid.shape[2:]
        k = np.ones(kShape)
        import pdb; pdb.set_trace()
        out = convolve(grid, k, mode='constant', cval=0.0)
        return out


#class PointCountCategories(ar.Aggregator):
#    def aggregate(self, glyphset, info, screen):
#        points = glyphset.table
#        cats = np.unique(glyphset.data())
#
#        layers = []
#        for cat in cats:
#           subset = points[glyphset.data() == cat]
#           layer = np.histogram2d(subset[:, 0], subset[:, 1], screen)
#           layers = layers + [layer[0]]
#
#        dense = np.dstack(layers)
#        return dense
#
#    def rollup(self, *vals):
#        """NOTE: Assumes co-registration of categories..."""
#        return reduce(lambda x, y: x+y,  vals)
#

class PointCountCategoriesH(ar.Aggregator):
    def aggregate(self, glyphset, info, screen):
        points = glyphset.table
        cats = np.unique(glyphset.data())
        dims = screen + (len(cats+1),)
        data = np.hstack([points[:, 0:2], glyphset.data()[:, np.newaxis]])
        dense = np.histogramdd(data, dims)
        return dense[0]

    def rollup(self, *vals):
        """NOTE: Assumes co-registration of categories..."""
        return reduce(lambda x, y: x+y,  vals)


def is_identity_transform(vt):
    return vt == (0, 0, 1, 1)


def load_csv(filename, skip, xc, yc, vc):
    """Turn a csv file into a glyphset.

    This is a fairly naive regulary-expression based parser
    (it doesn't handle quotes, blank lines or much else).
    It is useful for getting simple datasets into the system.
    """
    import re
    source = open(filename, 'r')
    points = []
    data = []

    for i in range(0, skip):
        source.readline()

    for line in source:
        line = re.split("\s*,\s*", line)
        x = float(line[xc].strip())
        y = float(line[yc].strip())
        v = float(line[vc].strip()) if vc >= 0 else 1
        g = [x, y, 0, 0]
        points.append(g)
        data.append(v)

    source.close()
    return Glyphset(np.array(points, order="F"), np.array(data))


def load_hdf(filename, node, xc, yc, vc=None, cats=None):
    """
    Load a node from an HDF file.

    filename : HDF file to load
    node: Path to relevant HDF table
    xc: Name/index of the x column
    yc: Name/index of the y column
    vc: Name/index of the value column (if applicable)
    cats: List of expected categories. 
        If cats is an empty list, a coding will be automatically generated
        Any value not on the list will be assigned category equal to list lenght
        Ignored if vc is not supplied.
    """
    import pandas as pd
    table = pd.read_hdf(filename, node)
    points = table[[xc, yc]]
    a = np.array(points, order="F")
    z = np.zeros_like(a)
    c = np.hstack([a, z])

   
    if vc:
        data = table[vc] 
        data = np.array(data)
        if cats is not None and len(cats) == 0:
            cats = data.unique()   # returns sorted values!!
        codes = dict(zip(cats, xrange(len(cats))))
        if codes:
            defcat = len(cats)
            coded = [codes.get(cat, defcat) for cat in data]  # TODO: Remove this SEQUENTIAL op
            coded = np.array(coded)
    else:
        coded = None

    print("Loaded %d items" % len(c))

    # Is this copy needed?  After all, projection makes a copy too...
    #    maybe the input just needs to be CLOSE to a numpy array
    return Glyphset(c, coded)
