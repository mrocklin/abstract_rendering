"""
Operations that apply across a broad variety of categories.
"""

import core


class Id(core.Shader):
    """ Return the input unchanged.
     This DOES NOT make a copy.
     It is usually used a zero-cost placeholder.
    """

    def shade(self, grid):
        return grid
