#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the compareTriplets function below.
def compareTriplets(a, b):
    # Decompose the tuples for Alice and Bob
    i = 0
    a_points = 0
    b_points = 0
    
    # Check for every position, in one loop
    while i < 3:
        if a[i] > b[i]:
            a_points += 1
        elif b[i] > a[i]:
            b_points += 1
        i += 1

    # Return the sum of points for each other
    return (a_points, b_points) 


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    a = list(map(int, input().rstrip().split()))
    b = list(map(int, input().rstrip().split()))
    result = compareTriplets(a, b)
    fptr.write(' '.join(map(str, result)))
    fptr.write('\n')
    fptr.close()
