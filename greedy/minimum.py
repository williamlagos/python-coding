#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the minimumAbsoluteDifference function below.
def minimumAbsoluteDifference(arr):
    minimum = sys.maxsize
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            res = abs(arr[i] - arr[j])
            if res < minimum: minimum = res
    return minimum

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(input())
    arr = list(map(int, input().rstrip().split()))
    result = minimumAbsoluteDifference(arr)
    fptr.write(str(result) + '\n')
    fptr.close()