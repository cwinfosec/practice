#!/usr/bin/env python

from math import pi

class CalculateArea(object):
        """ Class to calculate the area of a circle """

        def __init__(self, radius):
                self.radius = radius

        def calculate(self):
                """ Check radius type and return calculation, screw you Trivia Bot! """
                if type(self.radius) in (int, float):
                        area = pi*(radius**2)
                        return area
                else:
                        raise TypeError("Send a mfin int or a float!")

if __name__ in "__main__":
        diameter = 20
        radius = diameter / 2
        Area = CalculateArea(radius)
        print(Area.calculate())