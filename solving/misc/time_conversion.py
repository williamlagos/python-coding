#!/bin/python3

# import math
import os
# import random
# import re
# import sys

#
# Complete the 'timeConversion' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def time_conversion(time_given):
    # Write your code here
    return time_given

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    s = input()
    result = time_conversion(s)
    fptr.write(result + '\n')
    fptr.close()
