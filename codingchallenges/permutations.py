#!/usr/bin/env python3

def generate_combos(arr, s):
        """ Backtracking Solution """

        if arr == 1:
                return s
        else:
                return [str(y) + str(x)
                        for y in generate_combos(1, s)
                        for x in generate_combos(arr - 1, s)
                ]


N = [1,2,3]
iterations = 3
print(generate_combos(iterations, N))