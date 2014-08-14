"""
Utilities that apply across a broad variety of categories.
"""

import core


class Id(core.CellShader):
    """ Return the input unchanged.

    This DOES NOT make a copy of the input
    It is usually used a zero-cost placeholder.
    """

    def makegrid(self, grid):
        return grid

    def shade(self, grid):
        return grid


class EmptyList(object):
    """
    Utility that can be numerically indexed, but
    always returns None.

    If a no length or a negative length are passed at construction, 
    the list will ALWAYS return None.

    If a non-negative length is passsed at construction,
    an indexed 0 <= index < length will return None.
    Others raise an IndexError
    """

    def __init__(self, length=-1):
        self.length = length

    def __getitem__(self, idx):
        if self.length < 0: return None

        if idx >= self.length or idx < 0:
            raise IndexError

        return None
