#!/usr/bin/env python3
import string
import random
import sys

def generate_password(length):
        array_store = []
        for i in range(0,length):
                random_letter = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation))
                array_store += random_letter
        return ''.join(array_store)

length = int(sys.argv[1])
print(generate_password(length))