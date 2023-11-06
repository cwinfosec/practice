#!/usr/bin/env python3
import sys

ARGUMENT = int(sys.argv[1])

def fizzbuzz(n):
        """ Fizzbuzz Generator """

        if (n % 3 == 0 and n % 5 == 0):
                return f'fizzbuzz' * n
        if (n % 3 == 0):
                return f'fizz' * n
        if (n % 5 == 0):
                return f'buzz' * n
        else:
                return 'Invalid'

print(f'{fizzbuzz(ARGUMENT)}')
