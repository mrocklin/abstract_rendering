from blaze import Data, floor, into, compute, by, merge
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
    array([ 0,  2,  4,  6,  8, 10])

    And for time

    >>> binrange(np.datetime64('2000-12-28'), np.datetime64('2001-02-22'), 1, 'week')
    array(['2000-12-28', '2001-01-04', '2001-01-11', '2001-01-18',
           '2001-01-25', '2001-02-01', '2001-02-08', '2001-02-15', '2001-02-22'], dtype='datetime64[W]')

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
    (array([0, 2, 4, 6]), array([ 2.,  1.,  1.,  1.]))

    For datetime handling provide a measure (1) and a unit (month)

    >>> data = [date(2000, 1, 1), date(2001, 2, 2), date(2001, 1, 2)]
    >>> bins, values = bin1d(data, 1, 'month')
    >>> bins
    array(['2000-01', '2000-02', '2000-03', '2000-04', '2000-05', '2000-06',
           '2000-07', '2000-08', '2000-09', '2000-10', '2000-11', '2000-12',
           '2001-01', '2001-02'], dtype='datetime64[M]')
    >>> values
    array([ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  1.])
    """
    if not isinstance(data, Expr):
        data = Data(data, name='vals')

    start = compute(data.min().truncate(*binargs))
    stop = compute(data.max().truncate(*binargs))
    bins = binrange(start, stop, *binargs)

    expr = data.truncate(*binargs).count_values()
    result = into(np.ndarray, expr)

    counts = np.zeros(bins.shape)
    inds = np.searchsorted(bins, result[expr.fields[0]].astype(bins.dtype))
    counts[inds] = result['count']
    return bins, counts


def _bound(arr, x):
    arr[arr > x] = x
    return arr

def bin(expr, dimensions, **kwargs):
    """
    Split apply combine targetting regular grid

    Parameters
    ----------

    expr : blaze Expression
        The dataset on which you'd like to operate
    dimensions : list of tuples of column/truncation args
        sequence of tuples like (expr.latitude, 0.1) to determine binning
    **kwargs : Reductions to perform
        Reductions to perform using standard by or summary syntax

    >>> x = Data([1, 1, 2, 3, 4, 8])
    >>> bins, values = bin(x, [(x, 2)], count=x.count(), total=x.sum())
    >>> bins
    [array([0, 2, 4, 6, 8])]
    >>> values
    array([(2, 2), (2, 5), (1, 4), (0, 0), (1, 8)],
          dtype=[('count', '<i4'), ('total', '<i8')])
    """
    dims = [binrange(compute(d[0].min().truncate(*d[1:])),
                     compute(d[0].max().truncate(*d[1:])),
                     *d[1:]) for d in dimensions]

    expr = by(merge(*[d[0].truncate(*d[1:]) for d in dimensions]), **kwargs)
    computed = into(np.ndarray, expr)

    inds = tuple([_bound(
        np.searchsorted(dims[i],
                        computed[expr.fields[i]].astype(dims[i].dtype)),
                    len(dims[i]) - 1)
                for i in range(len(dims))])

    result = np.zeros(sum([d.shape for d in dims], ()),
                      dtype=computed.dtype.descr[-len(kwargs):])

    result[inds] = computed[expr.fields[-len(kwargs):]]
    return dims, result
