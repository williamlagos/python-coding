#!/usr/bin/env python3
# print('Hello World!')

import math
import os
import random
import re
import sys

# Complete the repeatedString function below.
def repeatedString(s, n):
    return ''

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    s = input()
    n = int(input())
    result = repeatedString(s, n)
    fptr.write(str(result) + '\n')
    fptr.close()