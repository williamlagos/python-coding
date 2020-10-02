#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the rotLeft function below.
def rotLeft(a, d):
    # Constraints check
    array = []
    array_size = len(a)
    if d > array_size or d < 1:
        return array
    
    # Rotation procedure
    array = a[d:] + a[:d]
    return array

if __name__ == '__main__':
    fptr = open('./output.txt' if 'OUTPUT_PATH' not in os.environ else os.environ['OUTPUT_PATH'], 'w')
    nd = input().split()
    n = int(nd[0])
    d = int(nd[1])
    a = list(map(int, input().rstrip().split()))
    result = rotLeft(a, d)
    fptr.write(' '.join(map(str, result)))
    fptr.write('\n')
    fptr.close()