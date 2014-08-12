from __future__ import print_function
import blaze as blz
import numpy as np
import abstract_rendering.glyphset as glyphset
import abstract_rendering.core as ar


class Glyphset(glyphset.Glyphset):
    def __init__(self, table, xcol, ycol, valcol, vt=(0, 0, 1, 1)):
        self._table = table
        self.xcol = xcol
        self.ycol = ycol
        self.valcol = valcol
        self.vt = vt
        self.shaper = glyphset.ToPoint(glyphset.item(xcol), glyphset.item(ycol))
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
        sparse = blz.by(points,
                        points[['__x', '__y']],
                        points[glyphset.valcol].count())
        sparse = blz.into(np.ndarray, sparse)
        sparse = sparse.astype(np.int32) #HACK: Having problems getting int32

        dense = np.empty((sparse[:, 0].max() + 1, sparse[:, 1].max() + 1), dtype=np.int64)
        dense[sparse[:, 0], sparse[:, 1]] = sparse[:, 2]
        return dense

    def rollup(self, *vals):
        return reduce(lambda x, y: x+y,  vals)




class Sum(ar.Aggregator):
    "Blaze sepcific implementation of the sum aggregator"

    def aggregate(self, glyphset, info, screen):
        #TODO: Handle sum.  Generate a new synthetic column based with info(valcol) and sum it
        points = glyphset.table
        sparse = blz.by(points,
                        points[['__x', '__y']],
                        points[glyphset.valcol].sum())
        sparse = blz.into(np.ndarray, sparse)
        sparse = sparse.astype(np.int32) #HACK: Having problems getting int32

        dense = np.empty((sparse[:, 0].max() + 1, sparse[:, 1].max() + 1), dtype=np.int64)
        dense[sparse[:, 0], sparse[:, 1]] = sparse[:, 2]
        return dense
    
    def rollup(self, *vals):
        return reduce(lambda x, y: x+y,  vals)


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
