#!/usr/bin/env python3
import math
import os
import random
import re
import sys

# Complete the 'waysToChooseSum' function below.
#
# The function is expected to return a LONG_INTEGER_ARRAY.
# The function accepts following parameters:
#  1. LONG_INTEGER a
#  2. LONG_INTEGER b

from collections import defaultdict

def waysToChooseSum(a, b):
    # Write your code here
    def sum_digits(n): # calculate the sum of digits of each coupon
        r = 0
        while n:
            r, n = r + n % 10, n // 10
        return r    
    
    sum_coupon = [ sum_digits(i) for i in range(a, b + 1) ]    
    d = defaultdict(int)
    for i in sum_coupon: d[i] +=1 
    
    max_list = []
    max_count = 1 # maximum of the counter 
    for i in d.keys():
        if d[i] == max_count:
            max_list.append(i)
        elif d[i] > max_count:
            max_count = d[i]
            max_list[:] = [] # clear previous list
            max_list.append(i)
        
    return(len(max_list), max_count)
    
if __name__ == '__main__':
    print(waysToChooseSum(1, 10))
    print(waysToChooseSum(1, 5))