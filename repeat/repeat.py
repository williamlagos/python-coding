#!/usr/bin/env python3
# print('Hello World!')

import math
import os
import random
import re
import sys

# Complete the repeatedString function below.
def repeatedString(s, n):
    
    characters = 0

    # Checks for empty a's on string
    if s.count('a') == 0: 
        return characters

    # If there is a, check if the string has same a's on all string extension
    string_length = len(s)
    if s == string_length * s[0]:
        return n
    
    # Mixed case - a's and other characters - handling
    a_single_quantity = s.count('a')
    complete_sequences = n // string_length
    remaining_sequence_slice = n % string_length
    
    characters = (complete_sequences * a_single_quantity) + s[:remaining_sequence_slice].count('a')
    
    return characters

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    s = input()
    n = int(input())
    result = repeatedString(s, n)
    fptr.write(str(result) + '\n')
    fptr.close()