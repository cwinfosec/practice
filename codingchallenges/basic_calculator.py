#!/usr/bin/env python3
import sys

class Calculator(object):

        def __init__(self, num1, num2):
                self.num1 = num1
                self.num2 = num2

        def add(self):
                return self.num1 + self.num2

        def subtract(self):
                return self.num1 - self.num2

        def multiply(self):
                return self.num1 * self.num2

        def divide(self):
                return self.num1 / self.num2

if __name__ in "__main__":
        num1 = int(sys.argv[1])
        num2 = int(sys.argv[2])
        calculate = Calculator(num1, num2)
        print("{} + {} = {}".format(num1, num2, calculate.add()))
        print("{} - {} = {}".format(num1, num2, calculate.subtract()))
        print("{} x {} = {}".format(num1, num2, calculate.multiply()))
        print("{} / {} = {}".format(num1, num2, calculate.divide()))