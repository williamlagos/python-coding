#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the isBalanced function below.
def isBalanced(s):
    opn = []
    enc = []
    enclosing = False
    for c in s:

        if '{' == c or '[' == c or '(' == c:
            opn.append(c)
            enclosing = False
        elif '}' == c or ']' == c or ')' == c: 
            enc.append(c)
            enclosing = True

        if enclosing:
            t = opn[-1:][0]
            if t == '{' and c == '}' or t == '[' and c == ']' or t == '(' and c == ')':
                opn.pop()
                enc.pop()

    return 'NO' if opn or enc else 'YES'

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    t = int(input())
    for t_itr in range(t):
        s = input()
        result = isBalanced(s)
        fptr.write(result + '\n')
    fptr.close()
