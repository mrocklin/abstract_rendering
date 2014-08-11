import blaze as blz
import numpy as np
import abstract_rendering.glyphset as glyphset
import abstract_rendering.core as ar



class Glyphset(glyphset.Glyphset):
    def __init__(array, shaper, valuer):
        if not isinstance(shaper, glyphset.ToPoint):
            raise ValueError("Blaze only works with point-based representation (pending a blaze flatmap)")

        super(glyphset.Glyphset, self).__init__(array, shaper, valuer)

    def points(self):
        pass

    def data(self):
        pass

    def bounds(self):
        pass



class Count(ar.Aggregator):
    "Blaze sepcific implementation of the count aggregator"
    pass

class Sum(ar.Aggregator):
    "Blaze sepcific implementation of the sum aggregator"
    pass


# Perhaps a blaze-grid?  Would require grid to be a wrapper around np array...
#      would provide also place for category mappings to live...
# Perhaps a blaze-transfer.  Could work with cellFunc already (probably)....
#    maybe add that to all transfers, and the numpy version is "special"....
#    is this like a numpy ufunc...maybe all of the shaders should be coded as ufuncs....
# If not a blaze-transfer, the blaze aggregator needs to return something that has been made dense.
