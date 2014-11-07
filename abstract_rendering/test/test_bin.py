from abstract_rendering.bin import *
from datetime import date


def eq(a, b):
    e = a == b
    if isinstance(e, np.ndarray):
        return e.all()
    else:
        return e

def test_binrange():
    assert eq(binrange(0, 10, 2), np.array([0,  2,  4,  6,  8, 10]))

    result = binrange(np.datetime64('2001-01-01'),
                       np.datetime64('2001-02-26'),
                       1, 'week')

    expected = np.array(['2000-12-28', '2001-01-04', '2001-01-11', '2001-01-18',
                         '2001-01-25', '2001-02-01', '2001-02-08', '2001-02-15',
                         '2001-02-22'], dtype='datetime64[D]')
    assert eq(result, expected)


def test_bin_1d():
    bins, counts = bin1d([1, 2, 1, 4, 5, 6], 2)
    assert list(bins) == [0, 2, 4, 6]
    assert list(counts) == [2, 1, 2, 1]


def test_bin_1d_with_empty_bins():
    bins, counts = bin1d([1, 2, 3, 10], 2)
    assert list(bins) == [0, 2, 4, 6, 8, 10]
    assert list(counts) == [1, 2, 0, 0, 0, 1]


def test_bin_1d_dates():
    bins, counts = bin1d([date(2000, 1, 1), date(2001, 2, 2), date(2001, 1, 2)],
                         1, 'year')
    assert list(bins) == [date(2000, 1, 1), date(2001, 1, 1)]
    assert list(counts) == [1, 2]

    bins, counts = bin1d([date(2000, 1, 1), date(2001, 2, 2), date(2001, 1, 2)],
                         1, 'month')
    assert eq(bins, np.arange(np.datetime64('2000-01', 'M'),
                              np.datetime64('2001-03', 'M'),
                              np.timedelta64(1, 'M')))
    assert list(counts) == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]

    bins, counts = bin1d([date(2001, 1, 1), date(2001, 2, 2), date(2001, 1, 2)],
                         5, 'days')
    assert bins.tolist() == [date(2000, 12, 31), date(2001, 1, 5),
            date(2001, 1, 10), date(2001, 1, 15), date(2001, 1, 20),
            date(2001, 1, 25), date(2001, 1, 30)]
    assert list(counts) == [2, 0, 0, 0, 0, 0, 1]


def test_bin():
    x = Data([1, 1, 2, 3, 4, 8])
    [bins], vals = bin(x, [(x, 2)], total=x.sum())
    vals = vals[vals.dtype.names[0]]
    assert eq(bins, [0, 2, 4, 6, 8])
    assert eq(vals, [2, 5, 4, 0, 8])

    [bins], vals = bin(x, [(x, 2)], count=x.count())
    vals = vals[vals.dtype.names[0]]
    assert eq(bins, [0, 2, 4, 6, 8])
    assert eq(vals, [2, 2, 1, 0, 1])

    [bins], vals = bin(x, [(x, 2)], count=x.count(), total=x.sum())
    assert eq(bins, [0, 2, 4, 6, 8])
    assert eq(vals, np.array([(2, 2), (2, 5), (1, 4), (0, 0), (1, 8)],
                             dtype=[('count', 'i4'), ('total', 'i8')]))

    [bins], vals = bin(x, [(x, 3)], count=x.count(), total=x.sum())
    assert eq(bins, [0, 3, 6])
    assert eq(vals, np.array([(3, 4), (2, 7), (1, 8)],
                             dtype=[('count', 'i4'), ('total', 'i8')]))


def test_bin_nd():
    data = [(i, j, i + j) for i in range(4) for j in range(4)]
    x = Data(data, dshape='16 * {a: int, b: int, c: int}')

    bins, vals = bin(x, [(x.a, 2), (x.b, 2)], total=x.c.sum(), count=x.c.count())

    expected = np.array([[(4, 4),  (4, 12)],
                         [(4, 12), (4, 20)]],
                        dtype=[('count', 'i4'), ('total', 'i4')])

    assert eq(vals, expected)
