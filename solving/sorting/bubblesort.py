#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the countSwaps function below.
def countSwaps(a):
    n = len(a)
    # Constraints check
    if n > 600:
        return
    # Bubble sort algorithm with swaps counting
    last = n - 1
    numSwaps = 0
    arraySorted = False
    while not arraySorted:
        i = 0
        while i < last:
            arraySorted = True
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                arraySorted = False
                numSwaps += 1
            i += 1
    print("Array is sorted in %d swaps.\nFirst Element: %d\nLast Element: %d" % (numSwaps, a[0], a[last]))


if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().rstrip().split()))
    countSwaps(a)
