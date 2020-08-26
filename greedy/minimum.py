#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the minimumAbsoluteDifference function below.
def minimumAbsoluteDifference(arr):
    minimum = sys.maxsize
    arr.sort()
    for i in range(1, len(arr)):
        res = abs(arr[i - 1] - arr[i])
        if res < minimum: minimum = res
    # print(minimum)
    return minimum

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(input())
    arr = list(map(int, input().rstrip().split()))
    result = minimumAbsoluteDifference(arr)
    fptr.write(str(result) + '\n')
    fptr.close()