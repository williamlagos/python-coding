#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the maxSubsetSum function below.
def maxSubsetSum(arr):
    including = 0
    excluding = 0
     
    for item in arr: 
        # Current max excluding item
        new_excluding = excluding if excluding > including else including
         
        # Current max including item 
        including = excluding + item 
        excluding = new_excluding
      
    # return max of including and excluding
    return (excluding if excluding > including else including) 

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(input())
    arr = list(map(int, input().rstrip().split()))
    res = maxSubsetSum(arr)
    fptr.write(str(res) + '\n')
    fptr.close()
