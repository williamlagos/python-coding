#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the roadsAndLibraries function below.
def roadsAndLibraries(n, c_lib, c_road, cities):
    min_cost = 0
    # Check if the cost of building a library is cheaper than a road
    if c_lib <= c_road:
        min_cost = n * c_lib
    else:
        # Else, prepare the graph algorithm
        c_areas = []
        for city in cities:
            # Check for empty city areas, then create the first one:
            if not c_areas:
                c_areas.append(set(city))
            else:
                i_areas = 0
                while i_areas < len(c_areas):
                    # Check for any difference by intersection on all areas
                    points = set(city).difference(c_areas[i_areas])
                    if len(points) == 1:
                        c_areas[i_areas] = c_areas[i_areas].union(points)
                        break
                    elif len(points) == 2:
                        c_areas.append(set(city))
                        break
                    else:
                        i_areas += 1

        unique_areas = []
        for area in c_areas:
            count = 0
            while count < len(c_areas):
                if len(set(area).difference(c_areas[count])) == 1:
                    unique_areas.append(area.union(c_areas[count]))
                count += 1
        
        if not unique_areas:
            unique_areas = c_areas
    
        num_roads = 0
        num_librs = len(unique_areas)
        for area in unique_areas:
            num_roads += len(area)
        min_cost = num_roads + num_librs
    
    return min_cost

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    q = int(input())
    for q_itr in range(q):
        nmC_libC_road = input().split()
        n = int(nmC_libC_road[0])
        m = int(nmC_libC_road[1])
        c_lib = int(nmC_libC_road[2])
        c_road = int(nmC_libC_road[3])
        cities = []
        for _ in range(m):
            cities.append(list(map(int, input().rstrip().split())))
        result = roadsAndLibraries(n, c_lib, c_road, cities)
        fptr.write(str(result) + '\n')
    fptr.close()