#!/usr/bin/env python3

import math
import os
import random
import re
import sys

#
# Complete the 'diagonalDifference' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY arr as parameter.
#

def diagonalDifference(arr):
    # Write your code here
    r = 0
    n = len(arr)
    i = 0
    j = n - 1
    i_sum = 0
    j_sum = 0
    # Checks if the 2D array have 
    # different number of columns
    if len(arr[0]) != n:
        return
    while r < n:
        i_sum += arr[r][i]
        j_sum += arr[r][j]
        r += 1
        i += 1
        j -= 1
    return abs(i_sum - j_sum)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(input().strip())
    arr = []
    for _ in range(n):
        arr.append(list(map(int, input().rstrip().split())))
    result = diagonalDifference(arr)
    fptr.write(str(result) + '\n')
    fptr.close()
