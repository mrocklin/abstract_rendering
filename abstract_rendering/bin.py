from blaze import Data, floor, into
from blaze.expr import Expr
from datashape import isnumeric
from datetime import date
import numpy as np
import blaze
from numbers import Number


def bin1d(x, binsize, scope=None):
    """ Bin data by binsize

    >>> x = [1, 2, 1, 5, 6]
    >>> bin1d(x, 2)
    (array([0, 2, 4, 6], dtype=int32), array([2, 1, 1, 1], dtype=int32))

    >>> x = [date(2000, 1, 1), date(2001, 2, 2), date(2001, 1, 2)]
    >>> bin1d(x, blaze.year)
    (array([2000, 2001], dtype=int32), array([1, 2], dtype=int32))
    """
    if not isinstance(x, Expr):
        x = Data(x)

    if (isinstance(binsize, type) and issubclass(binsize, Expr) or
        callable(binsize) and binsize.__name__ in dir(x)):
        f = binsize
        binsize = f(x)
        binsexpr = f(x).distinct().sort(binsize._name)

    if isinstance(binsize, Number) and isnumeric(x.dshape):
        n = binsize
        binsize = floor(x / n)
        binsexpr = floor((binsize * n).distinct().sort(binsize._name))

    assert isinstance(binsize, Expr) and x in binsize

    countsexpr = binsize.count_values().sort(binsize._name).count

    bins = into(np.ndarray, binsexpr)
    counts = into(np.ndarray, countsexpr)

    return bins, counts

# TODO: This doesn't fill in bins with 0 counts
