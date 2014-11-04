from blaze import Data, floor, into
from blaze.expr import Expr
from datashape import isnumeric
from datetime import date
import numpy as np
import blaze
from numbers import Number


def bin1d(data, binsize, scope=None):
    """ Bin data by binsize

    Parameters
    ----------

    data: Anything Blaze understands
        Array to bin
    binsize: Number or Blaze function or Blaze expression
        size of a bin

    Examples
    --------

    In basic use, binsize can be just the size of a numeric bin.  Here bins are
    of size two.

    >>> data = [1, 2, 1, 5, 6]
    >>> bin1d(data, 2)
    (array([0, 2, 4, 6], dtype=int32), array([2, 1, 1, 1], dtype=int32))

    Alternatively provide a blaze function.  This function will be applied to
    control the binning

    >>> data = [date(2000, 1, 1), date(2001, 2, 2), date(2001, 1, 2)]
    >>> bin1d(data, blaze.year)
    (array([2000, 2001], dtype=int32), array([1, 2], dtype=int32))

    Or, if your data is already an interactive blaze expression

    >>> data = blaze.Data([date(2000, 1, 1), date(2001, 2, 2), date(2001, 1, 2)])

    Then just provide an expression over which to bin

    >>> bin1d(data, data.month)
    (array([1, 2], dtype=int32), array([2, 1], dtype=int32))
    """
    if not isinstance(data, Expr):
        data = Data(data)

    if (isinstance(binsize, type) and issubclass(binsize, Expr) or
        callable(binsize) and binsize.__name__ in dir(data)):
        f = binsize
        binsize = f(data)
        binsexpr = f(data).distinct().sort(binsize._name)

    elif isinstance(binsize, Number) and isnumeric(data.dshape):
        n = binsize
        binsize = floor(data / n)
        binsexpr = floor((binsize * n).distinct().sort(binsize._name))

    elif isinstance(binsize, Expr):
        binsexpr = binsize.distinct().sort(binsize._name)

    assert isinstance(binsize, Expr) and data in binsize

    countsexpr = binsize.count_values().sort(binsize._name).count

    bins = into(np.ndarray, binsexpr)
    counts = into(np.ndarray, countsexpr)

    return bins, counts

# TODO: This doesn't fill in bins with 0 counts
