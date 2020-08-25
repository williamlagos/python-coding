#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the makeAnagram function below.
def makeAnagram(a, b):
    return ''

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    a = input()
    b = input()
    res = makeAnagram(a, b)
    fptr.write(str(res) + '\n')
    fptr.close()
