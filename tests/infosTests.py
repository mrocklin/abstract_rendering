from __future__ import print_function

import unittest
import abstract_rendering.infos as infos


class Const(unittest.TestCase):
    def test(self):
        info = infos.const(3)

        self.assertTrue(callable(info))
        self.assertEqual(3, info(3,3))
        self.assertEqual(3, info(None,23))
        self.assertEqual(3, info("", None))
        self.assertEqual(3, info([2, 4, 3], []))
        self.assertEqual(3, info(object(), self))


class Val(unittest.TestCase):
    def test(self):
        info = infos.val(15)

        self.assertTrue(callable(info))
        self.assertEqual(3, info(0, 3))
        self.assertEqual(0, info(3, 0))
        self.assertEqual(15, info(3, None))


class ValAt(unittest.TestCase):
    def test(self):
        info = infos.valAt(3, "Nothing")

        self.assertTrue(callable(info))
        self.assertEqual(3, info(None, [0, 1, 2, 3]))
        self.assertEqual("three", info(None, ["zero", "one", "two", "three"]))
        self.assertEqual("Nothing", info(None, None))
        self.assertEqual("Nothing", info(None, []))
        self.assertEqual("Nothing", info(None, [1,2]))

class Key(unittest.TestCase):
    def test(self):
        info = infos.key("val", "seven")

        self.assertTrue(callable(info))
        self.assertEqual(3, info(None, {"val": 3, "other": 6}))
        self.assertEqual("seven", info(None, {"value": 3, "other": 6}))

class Attribute(unittest.TestCase):

    class Has():
        val = 13
        other= 6
    
    class HasNot():
        value = 13
        other= 6

    def test(self):
        info = infos.attribute("val", "seven")

        self.assertTrue(callable(info))
        self.assertEqual(13, info(None, self.Has()))
        self.assertEqual("seven", info(None, self.HasNot()))


if __name__ == '__main__':
    unittest.main()
