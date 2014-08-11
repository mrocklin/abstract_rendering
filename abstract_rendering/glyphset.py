import numpy as np
import re


def enum(**enums): return type('Enum', (), enums)
ShapeCodes = enum(POINT=0, LINE=1, RECT=2)
# TODO: Add shapecodes: CIRCLE, POINT_RECT, POINT_CIRCLE, etc


class Glyphset(object):
    """shaper + shape-params + associated data ==> Glyphset

       fields:
       _points : Points held by this glyphset
       _data : Data associated with the points (basis for 'info' values).
               _points[x] should associate with data[x]
       shapecode: Shapecode that tells how to interpret _points

    """
    _points = None
    _data = None
    shaper = None

    def __init__(self, points, data, shaper, colMajor=False):
        self._points = points
        self._data = data
        self.shaper = shaper
        self.shaper.colMajor = colMajor  # HACK: This modification is bad form...would rather do a copy

    # TODO: Add the ability to get points m...n
    def points(self):
        """Returns the set of [x,y,w,h] points for this glyphset.
           Access to raw data is through _points.
        """

        if (type(self.shaper) is Literals):
            if type(self._points) is list:
                return np.array(self._points, order="F")
            elif type(self._points) is np.ndarray:
                return self._points
            else:
                ValueError("Unhandled (literal) points type: %s"
                           % type(self._points))
        else:
            # TODO: Setup the shaper utilities to go directly to fortran order
            return np.array(self.shaper(self._points), order="F")

    def project(viewxform):
        """Project the points found in the glyphset according to the view transform.

        viewxform -- convert canvas space to pixel space [tx,ty,sx,sy]
        returns a new new glyphset with projected points and associated info values
        """
        points = glyphs.points()
        out = np.empty_like(points, dtype=np.int32)
        _projectRects(viewxform, points, out)

        # Ensure visilibity, make sure w/h are always at least one
        # TODO: There is probably a more numpy-ish way to do this...(and it might not be needed for Shapecode.POINT)
        for i in xrange(0, out.shape[0]):
            if out[i, 0] == out[i, 2]:
                out[i, 2] += 1
            if out[i, 1] == out[i, 3]:
                out[i, 3] += 1

        return glyphset.Glyphset(out, glyphs.data(),
                                 glyphset.Literals(glyphs.shaper.code))


    def data(self):
        return self._data

    def bounds(self):
        """Compute bounds of the glyph-set.  Returns (X,Y,W,H)

           Assumes a 'simple' layout where the min and max input values
           determine the min and max positional values.
        """
        minX = float("inf")
        maxX = float("-inf")
        minY = float("inf")
        maxY = float("-inf")
        for g in self.points():
            (x, y, w, h) = g

            minX = min(minX, x)
            maxX = max(maxX, x+w)
            minY = min(minY, y)
            maxY = max(maxY, y+h)
        return (minX, minY, maxX-minX, maxY-minY)
#        points = self.points();
#        minX=points[:,0].min()
#        maxX=points[:,0].max()
#        minY=points[:,1].min()
#        maxY=points[:,1].max()
#        maxW=points[:,2].max()
#        maxH=points[:,3].max()
#
#        shapes = self.shaper([[minX,maxX],[minY,maxY],[maxW,maxW],[maxH,maxH]])
#        minX = shapes[0][0]
#        minY = shapes[0][1]
#        maxX = shapes[1][0]
#        maxY = shapes[1][1]
#        width = shapes[1][2]
#        height = shapes[1][3]
#
#        return (minX, minY, maxX+width, maxY+height)


# Shapers.....
class Shaper(object):
    fns = None  # List of functions to apply
    code = None
    colMajor = False

    # TODO: When getting subsets of the data out of glyphset.points(), remove this colMajor and handle it up in glyphset instead
    def __call__(self, vals):
        if not self.colMajor:
            return [map(lambda f: f(val), self.fns) for val in vals]
        else:
            return [map(lambda f: f(val), self.fns) for val in zip(*vals)]


class Literals(Shaper):
    """Optimization marker, tested in Glyphset to skip conversions.
       Using this class asserts that the _points value of the Glyphset
       is the set of points to feed into a geometry renderer, and thus
       no projection from data space to canvas space is required.
       Use with caution...
    """
    def __init__(self, code):
        self.code = code

    def __call__(self, vals):
        return vals


class ToRect(Shaper):
    """Creates rectangles using functions to build x,y,w,h."""
    code = ShapeCodes.RECT

    def __init__(self, tox, toy, tow, toh):
        self.fns = [tox, toy, tow, toh]


class ToLine(Shaper):
    """Creates lines using functions to build x1,y1,x2,y2"""
    code = ShapeCodes.LINE

    def __init__(self, tox1, toy1, tox2, toy2):
        self.fns = [tox1, toy1, tox2, toy2]


class ToPoint(Shaper):
    """Create a single point, using functions to build x,y,0,0
       Can accept more than just tox/toy arguments, but ignores them.
    """
    code = ShapeCodes.POINT

    def __init__(self, tox, toy, *args):
        self.fns = [tox, toy, lambda x: 0, lambda x: 0]


# Utilities for shapers....
def const(v):
    """Create a function that always returns a specific value.

    * v -- The value the returned function always returns
    """
    def f(a):
        return v
    return f


def item(i):
    """
    Get items out of a collection.  
    Suiteable for use with numerically indexed (i.e., array)
    or object-indexed (i.e., dictionary) sources.

    * i -- The item parameter that will be used
    """
    def f(a):
        return a[i]
    return f


def load_csv(filename, skip, xc, yc, vc, width, height, shapecode):
    """Turn a csv file into a glyphset.

    This is a fairly naive regulary-expression based parser
    (it doesn't handle quotes, blank lines or much else).
    It is useful for getting simple datasets into the system.
    """
    source = open(filename, 'r')
    glyphs = []
    data = []

    if shapecode is ShapeCodes.POINT:
        width = 0
        height = 0

    for i in range(0, skip):
        source.readline()

    for line in source:
        line = re.split("\s*,\s*", line)
        x = float(line[xc].strip())
        y = float(line[yc].strip())
        v = float(line[vc].strip()) if vc >= 0 else 1
        g = [x, y, width, height]
        glyphs.append(g)
        data.append(v)

    source.close()
    return Glyphset(glyphs, data, Literals(shapecode))
