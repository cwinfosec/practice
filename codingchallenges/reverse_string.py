#!/usr/bin/env python3

def reverse(some_string):
        """ List Solution """
        reversed_string = []

        for char in range(len(some_string)-1, -1, -1):
                reversed_string.append(some_string[char])

        return ''.join(reversed_string)

some_string = "noops on si ereht"
print(reverse(some_string))