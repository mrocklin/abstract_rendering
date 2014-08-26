from __future__ import print_function, division
import blaze as blz
import numpy as np
import abstract_rendering.glyphset as glyphset
import abstract_rendering.core as ar
import math

# TODO: Priveledges names be problematic.  Right now __x, __y, __info are used. 
#       Should probably do something gensym(<root>, <exclude_names>).  Where
#       gensym will return something based on <root> and not in <exclude_names>.
#       Then store those names in glyphset
class Glyphset(glyphset.Glyphset):
    def __init__(self, table, xcol, ycol, valcol, vt=(0, 0, 1, 1)):
        self._table = table
        self.xcol = xcol
        self.ycol = ycol
        self.valcol = valcol
        self.vt = vt
        self.shaper = glyphset.ToPoint(glyphset.idx(xcol),
                                       glyphset.idx(ycol))
        self.table = blz.merge(table,
                               ((table[xcol] * vt[2]) + vt[0]).label('__x'),
                               ((table[ycol] * vt[3]) + vt[1]).label('__y'))

    def points(self):
        return self.table[self.xcol, self.ycol]

    def data(self):
        return self.table[self.valcol]

    def project(self, vt):
        nvt = (self.vt[0]+vt[0],
               self.vt[1]+vt[1],
               self.vt[2]*vt[2],
               self.vt[3]*vt[3])
        return Glyphset(self._table, self.xcol, self.ycol, self.valcol, vt=nvt)

    def bounds(self):
        xmax = blz.compute(self.table['__x'].max())
        xmin = blz.compute(self.table['__x'].min())
        ymax = blz.compute(self.table['__y'].max())
        ymin = blz.compute(self.table['__y'].min())
        return (xmin, ymin, xmax-xmin, ymax-ymin)


class Count(ar.Aggregator):
    "Blaze sepcific implementation of the count aggregator"

    def aggregate(self, glyphset, info, screen):
        points = glyphset.table
        
        finite = blz.merge(points['__x'].map(math.floor, schema='{__x: int32}'),
                           points['__y'].map(math.floor, schema='{__y: int32}'),
                           points['__x'].map(lambda x: 1, schema='{__info: int32}'))
        sparse = blz.by(finite,
                        finite[['__x', '__y']],
                        finite['__info'].count())
        return to_numpy(sparse, screen, '__info_count')

    def rollup(self, *vals):
        return reduce(lambda x, y: x+y,  vals)


class Sum(ar.Aggregator):
    "Blaze sepcific implementation of the sum aggregator"

    def aggregate(self, glyphset, info, screen):
        points = glyphset.table
        
        schema = "{__info: %s}" % self.infotype
        infos = points[glyphset.valcol].map(info, schema=schema)
        finite = blz.merge(points['__x'].map(math.floor, schema='{__x: int32}'),
                           points['__y'].map(math.floor, schema='{__y: int32}'),
                           infos)

        sparse = blz.by(finite,
                        finite[['__x', '__y']],
                        finite['__info'].sum())
        return to_numpy(sparse, screen, '__info_sum')

    def rollup(self, *vals):
        return reduce(lambda x, y: x+y,  vals)


class CountCategories(ar.Aggregator):
    def __init__(self, info):
        self.infotype = info
        super(ar.Aggregator, self).__init__()

    def aggregate(self, glyphset, info, screen):
        points = glyphset.table

        schema = "{__info: %s}" % self.infotype
        infos = points[glyphset.valcol].map(info, schema=schema)
        cats = infos.distinct()

        finite = blz.merge(points['__x'].map(math.floor, schema='{__x: int32}'),
                           points['__y'].map(math.floor, schema='{__y: int32}'),
                           infos) 
        sparse = blz.by(finite,
                        finite[['__x', '__y', '__info']],
                        finite['__info'].count())

        items = []
        for cat in blz.compute(cats):
            subset = sparse[sparse['__info'] == cat]
            items.append(to_numpy(subset[['__x', '__y', '__info_count']], screen, '__info_count'))
        
        rslt = np.dstack(items)
        return rslt

    def rollup(self, *vals):
        """NOTE: Assumes co-registration of categories..."""
        return reduce(lambda x, y: x+y,  vals)


def to_numpy(sparse, screen=None, values='__info'):
    """
    Convert a blaze table to a numpy arary.
    Assumes table schema format is [x,y,val]

    TODO: Add screen_origin so a subset of the space can sliced out easily
    """
    if not screen:
        screen = (blz.compute(sparse['__x'].max()) + 1, blz.compute(sparse['__y'].max()) + 1)
    else:
        #Just things that fit on the screen
        sparse = sparse[sparse['__x'] < screen[0] and sparse['__y'] < screen[1]]
    
    (width, height) = screen

    xx = blz.into(np.ndarray, sparse.__x).astype(np.int32)
    yy = blz.into(np.ndarray, sparse.__y).astype(np.int32)
    vals = blz.into(np.ndarray, sparse[values])
    
    dense = np.zeros((height, width), dtype=vals.dtype)
    dense[yy, xx] = vals
    return dense


def load_csv(file, xc, yc, vc, **kwargs):
    """
    Produce point-based glyphs in a blaze-backed glyphset from a csv file.

    * File - name of a csv file to load
    * schema - scheam of the source file
    * xc - name of the column to use for x values
    * yc - name of column to use for y values
    * vc - name of column to use for info values
    """

    csv = blz.CSV(file, **kwargs)
    t = blz.Table(csv)
    return Glyphset(t, xc, yc, vc)


# Perhaps a blaze-grid?  Would require grid to be a wrapper around np array...
#      would provide also place for category mappings to live...
# Perhaps a blaze-transfer.  Could work with cellFunc already (probably)....
#    maybe add that to all transfers, and the numpy version is "special"....
#    is this like a numpy ufunc...maybe all of the shaders should be coded as ufuncs....
# If not a blaze-transfer, the blaze aggregator needs to return something that has been made dense.

# Problems with project:
#   Numpy version does it as a separate phase (in the main runner) an dit
#   is a hard-coded function call.  Blaze might be able to do it more efficiently using
#   its own expresions.  Add glyphset.project(vt) ---> glyphset. This may allow "points(self)" to be removed
