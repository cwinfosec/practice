#!/usr/bin/env python3

import sys

"""
f(x) = (n - 1) + (n - 2)
"""

def calculate(n):

        if n in {0, 1}:
                return n

        return calculate(n - 1) + calculate(n - 2)

if __name__ in "__main__":

        N = [1,2,3,4,5,6,7,8,9]
        for item in N:
                print(calculate(item), end=' ')