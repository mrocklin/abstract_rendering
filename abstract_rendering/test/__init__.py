from __future__ import print_function


def run_all():
    import unittest

    suite = unittest.defaultTestLoader.discover('.', pattern='*[T|t]est*.py')
    result = suite.run(unittest.TestResult())
    print(result)
    return result.wasSuccessful()

