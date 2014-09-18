from __future__ import print_function
import unittest

def run_all():
    suite = unittest.defaultTestLoader.discover('.', pattern='*[T|t]est*.py')
    result = suite.run(unittest.TestResult())
    print(result)
    return result.wasSuccessful()
