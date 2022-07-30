#!/usr/bin/env python3

import unittest
from temperature_convert import TempConverter

class TestConvert(unittest.TestCase):
        """ Unit test program for Temperature Converter """

        def test_convert(self):
                """ Runs a single test case for conversion """
                self.assertEqual(TempConverter(15).convert(), float(59))

        def test_type(self):
                """ Runs a single test case for return type """
                self.assertIsInstance(TempConverter(15).convert(), float)

        def test_invalids(self):
                """ Runs several test cases for invalid temperature values """
                self.assertRaises(AttributeError, TempConverter.convert, "test")
                self.assertRaises(AttributeError, TempConverter.convert, True)
                self.assertRaises(AttributeError, TempConverter.convert, 1+2j)
                self.assertRaises(AttributeError, TempConverter.convert, [1,2])

if __name__ in "__main__":
        unittest.main()