
"""Each info function returns a function that takes two arguments:
   shape and data. The 'shape' is the projected shape information.
   The 'data' is the data package associated with that information.
"""


def const(v):
    """Return the value passed."""
    def f(data):
        return v
    return f


def val(default=None):
    """Return the entire data value. This is the info-version of 'id'.
    """
    def f(data):
        if data is None:
            return default
        else:
            return data
    return f


def valAt(i, default=None):
    """Return the value at a given index in the data part of the input.
         On error returns the default value.
    """
    def f(data):
        try:
            return data[i]
        except:
            return default
    return f


def key(att, default=None):
    "Return the value under a given key in the data part of the input."
    def f(data):
        return data.get(att, default)
    return f


def attribute(att, default=None):
    "Return the value under a given attribute in the data part of the input."
    def f(data):
        return getattr(data, att, default)
    return f
