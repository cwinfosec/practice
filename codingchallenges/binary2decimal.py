#!/usr/bin/env python3

def convert_to_binary(n):
        if n > 1:
                convert_to_binary(n//2)
        print(f"{n % 2}", end='')

if __name__ in "__main__":
        decimal = 10
        convert_to_binary(decimal)