#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the makeAnagram function below.
def makeAnagram(a, b):
    # itr = [v for v in a if v in b] + [v for v in b if v in a]
    # inter = [itr.count(i) - (itr.count(i) % 2) for i in set(itr)]
    # mov = (len(a) + len(b)) - sum(inter)
    # print(mov)
    itr = set(a) & set(b)
    itr_cnt = 0
    for i in itr:
        a_times = a.count(i)
        b_times = b.count(i)
        if a_times < b_times:
            itr_cnt += a_times * 2 
        else:
            itr_cnt += b_times * 2
    mov = len(a + b) - itr_cnt
    # print(mov)
    return mov

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    a = input()
    b = input()
    res = makeAnagram(a, b)
    fptr.write(str(res) + '\n')
    fptr.close()
