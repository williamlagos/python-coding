#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the plusMinus function below.
def plusMinus(arr):
    r = [0, 0, 0]
    l = len(arr)
    # Iterate over array
    for i in arr:
        # Check if its lesser, equal, or bigger than zero
        if i > 0: r[0] += 1
        elif i < 0: r[1] += 1
        elif i == 0: r[2] += 1
    # Print the three ratios in order
    for i in r:
        print(i/l)

if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().rstrip().split()))
    plusMinus(arr)
