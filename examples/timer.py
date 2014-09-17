from __future__ import print_function, division, absolute_import
import time

class Timer(object):
    def __init__(self, name, verbose=True):
        self.verbose = verbose
        self.name = name

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print("{0} elapsed time: {1} ms".format(self.name, self.msecs))
