#!/usr/bin/env python3

import math
import os
import random
import re
import sys
import collections

# Complete the checkMagazine function below.
def checkMagazine(magazine, note):
    mgz_cnt = collections.Counter(magazine)
    not_cnt = collections.Counter(note)
    print('No') if len(not_cnt - mgz_cnt) > 0 else print('Yes')

if __name__ == '__main__':
    mn = input().split()
    m = int(mn[0])
    n = int(mn[1])
    magazine = input().rstrip().split()
    note = input().rstrip().split()
    checkMagazine(magazine, note)
