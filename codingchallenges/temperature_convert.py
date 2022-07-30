#!/usr/bin/env python3

class TempConverter(object):
        """ Class for converting Celsius to Fahrenheit """

        def __init__(self, n):
                # Seems wasteful to create another method below
                self.n = n

        def convert(self):
                """ Take the temperature in degrees Celsius and convert it to Fahrenheit """

                if type(self.n) in (int, float):
                        fahrenheit = self.n*9/5+32
                        return fahrenheit
                else:
                        raise AttributeError("Argument must be an int or float")

if __name__ in "__main__":
        n = [1,2]
        T = TempConverter(n)
        print(T.convert())