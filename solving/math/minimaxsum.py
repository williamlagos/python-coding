#!/usr/bin/env python3

import math
import os
import random
import re
import sys
import itertools

# Complete the miniMaxSum function below.
def miniMaxSum(arr):
    sums = []
    for subset in itertools.combinations(arr, 4):
        sums.append(sum(subset))
    print('%d %d' % (min(sums), max(sums)))

if __name__ == '__main__':
    arr = list(map(int, input().rstrip().split()))
    miniMaxSum(arr)