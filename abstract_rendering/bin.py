from blaze import Data, floor, into, compute
from blaze.expr import Expr
from blaze.expr.datetime import normalize_time_unit
from datashape import isnumeric
from datetime import date
import numpy as np
import blaze
from numbers import Number


timedelta_types = {'year': 'Y',
                   'month': 'M',
                   'week': 'W',
                   'day': 'D',
                   'hour': 'h',
                   'minute': 'm',
                   'second': 's',
                   'millisecond': 'ms',
                   'microsecond': 'us',
                   'nanosecond': 'ns'}

def binrange(start, stop, *binargs):
    """ Compute range of bins

    Works for arithmetic

    >>> binrange(0, 10, 2)
    array([0,  2,  4,  6,  8, 10])

    And for time

    >>> binrange(np.datetime64('2001-01-01'), np.datetime64('2001-02-26'), 1, 'week')
    array(['2001-01-01', '2001-01-08', '2001-01-15', '2001-01-22',
           '2001-01-29', '2001-02-05', '2001-02-12', '2001-02-19', '2001-02-26'], dtype='datetime64[D]')
    """
    if len(binargs) == 1:
        step = binargs[0]
    else:
        measure, unit = binargs
        typ = timedelta_types[normalize_time_unit(unit)]

        start = np.datetime64(start, typ)
        stop = np.datetime64(stop, typ)
        step = np.timedelta64(measure, typ)
    return np.arange(start, stop + step, step)


def bin1d(data, *binargs):
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

    >>> bin1d(data, 1, 'month')
    (array([1, 2], dtype=int32), array([2, 1], dtype=int32))
    """
    if not isinstance(data, Expr):
        data = Data(data, name='vals')

    start = compute(data.min().truncate(*binargs))
    stop = compute(data.max().truncate(*binargs))
    bins = binrange(start, stop, *binargs)

    expr = data.truncate(*binargs).count_values()
    result = into(np.ndarray, expr)

    counts = np.zeros(bins.shape)
    inds = np.searchsorted(bins, result[expr.fields[0]])
    counts[inds] = result['count']
    return bins, counts
