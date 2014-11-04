from abstract_rendering.bin import *
from datetime import date

def test_bin_1d():
    bins, counts = bin1d([1, 2, 1, 4, 5, 6], 2)
    assert list(bins) == [0, 2, 4, 6]
    assert list(counts) == [2, 1, 2, 1]


def test_bin_1d_dates():
    bins, counts = bin1d([date(2000, 1, 1), date(2001, 2, 2), date(2001, 1, 2)],
                         blaze.year)
    assert list(bins) == [2000, 2001]
    assert list(counts) == [1, 2]


    bins, counts = bin1d([date(2000, 1, 1), date(2001, 2, 2), date(2001, 1, 2)],
                         blaze.day)
    assert list(bins) == [1, 2]
    assert list(counts) == [1, 2]
