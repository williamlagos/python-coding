#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the jumpingOnClouds function below.
def jumpingOnClouds(c):
    jumps = 0

    # Constraints check
    clouds_quantity = len(c)
    if clouds_quantity < 2 or clouds_quantity > 100:
        return jumps
    if c[0] == 0 and c[-1:] == 0:
        return jumps

    ones = c.count(1)
    zeroes = c.count(0)
    clouds = ones + zeroes
    if ones >= zeroes:
        return jumps
    if clouds != clouds_quantity:
        return jumps

    # Logical construction
    i = 0
    last = clouds - 1
    while i < last: 
        # Checks the least adjacent
        one_step = i + 1
        two_step = i + 2
        if two_step <= last and c[two_step] == 0:
            jumps += 1
            i += 2
        # Checks for the nearer adjacent
        elif one_step <= last and c[one_step] == 0:
            jumps += 1
            i += 1
        # Ends the loop if any of these checks are invalid
        else: 
            i = last

    return jumps

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    # fptr = open('./output.txt', 'w')
    n = int(input())
    c = list(map(int, input().rstrip().split()))
    result = jumpingOnClouds(c)
    fptr.write(str(result) + '\n')
    fptr.close()
