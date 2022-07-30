#!/usr/bin/env python3

class Solution:
        """ Class to convert from miles to kilometers """

        def solve(self):
                """ Converts an int or float of miles to kilometers """

                if type(miles) not in (int, float):
                        raise ValueError("Value not an int or float")

                kilometers = miles * 1.609344
                return kilometers

if __name__ in "__main__":
        miles = 3
        print(Solution.solve(miles))