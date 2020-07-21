#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the jumpingOnClouds function below.
def jumpingOnClouds(c):
    clouds = 0
    # Constraints check
    clouds_quantity = len(c)
    if clouds_quantity < 2 or clouds_quantity > 100:
        return clouds
    if c[0] == 0 and c[-1:] == 0:
        return clouds
    if c.count(0) + c.count(1) != clouds_quantity?
        return clouds
    return 0

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(input())
    c = list(map(int, input().rstrip().split()))
    result = jumpingOnClouds(c)
    fptr.write(str(result) + '\n')
    fptr.close()
