#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the flippingBits function below.
def flippingBits(n):
    l = n.bit_length()
    bits = '1' * l if l > 0 else '0' * 1
    bitmask = int(bits, 2)
    return n ^ bitmask
        

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    q = int(input())
    for q_itr in range(q):
        n = int(input())
        result = flippingBits(n)
        fptr.write(str(result) + '\n')
    fptr.close()
