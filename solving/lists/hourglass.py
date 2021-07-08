#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Problem link: https://www.hackerrank.com/challenges/2d-array/problem
#
# Complete the 'hourglassSum' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY arr as parameter.
#

def hourglassSum(arr):
    # Write your code here
    m = len(arr)
    sums = []
    for x in range(m - 2):
        for y in range(m - 2):
            sums.append(sum([arr[x][y],      arr[x][y + 1],      arr[x][y + 2],
                                             arr[x + 1][y + 1],
                             arr[x + 2][y],  arr[x + 2][y + 1],  arr[x + 2][y + 2]]))
    return max(sums)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    arr = []
    for _ in range(6):
        arr.append(list(map(int, input().rstrip().split())))
    result = hourglassSum(arr)
    fptr.write(str(result) + '\n')
    fptr.close()
