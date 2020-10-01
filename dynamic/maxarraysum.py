#!/usr/bin/env python3

import math
import os
import random
import re
import sys

def powerSet(arr, itr):
    print(arr)
    if itr == 0:
        return arr
    else:
        itr -= 1
        powerSet(arr[1:], itr)

# Complete the maxSubsetSum function below.
def maxSubsetSum(arr):
    return ''

if __name__ == '__main__':
    powerSet([-2,1,3,-4,5],7)

# if __name__ == '__main__':
#     fptr = open(os.environ['OUTPUT_PATH'], 'w')
#     n = int(input())
#     arr = list(map(int, input().rstrip().split()))
#     res = maxSubsetSum(arr)
#     fptr.write(str(res) + '\n')
#     fptr.close()
