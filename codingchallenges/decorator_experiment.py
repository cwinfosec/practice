#!/usr/bin/env python3

from datetime import datetime
import time

def separator(func):
        def wrapper(*args, **kwargs):
                print("-------------------------")
                val = func(*args, **kwargs)
                return val
        return wrapper

def get_time(func):
        def timer(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                end = time.time()
                print(f"Program took {(end - start) * 1000}s to run")
                return result
        return timer

def logger(func):
        def inner(*args, **kwargs):
                print(f"Starting run at {datetime.now()}")
                print(f"Running {func.__name__}()")
                func(*args, **kwargs)
        return inner

@separator
def add(*args):
        count = 0
        for x in args:
                count += x
        return count

@separator
def subtract(*args):
        count = args[0]
        for x in args[1:]:
                count -= x
        return count

@separator
def divide(*args):
        if 0 in args:
                raise ValueError("Error - divide by zero.")
        count = args[0]
        for x in args[1:]:
                count /= x
        return count

@separator
def multiply(*args):
        count = 1
        for x in args:
                count *= x
        return count

print(f"4 + 5 + 1 = {add(4,5,1)}")
print(f"1 - 2 - 3 = {subtract(1,2,3)}")
print(f"5 x 5 x 5 = {multiply(5,5,5)}")
print(f"100 / 5 / 2 = {divide(100,5,2)}")