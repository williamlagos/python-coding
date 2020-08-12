#!/usr/bin/env python3

import math
import os
import random
import re
import sys

# Complete the roadsAndLibraries function below.
def roadsAndLibraries_imp1(n, c_lib, c_road, cities):
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
                # If there isn't any area, create the first one
                c_areas.append(set(city))
            else:
                i_areas = 0
                while i_areas < len(c_areas):
                    # Check for any difference by intersection on all areas
                    points = set(city).difference(c_areas[i_areas])
                    if len(points) == 1:
                        # If there is one intersection, add to its set
                        c_areas[i_areas] = c_areas[i_areas].union(points)
                        break
                    elif len(points) == 2:
                        # If not, create another set 
                        c_areas.append(set(city))
                        break
                    else:
                        i_areas += 1

        unique_areas = []
        # Make areas unique checking each other
        for area in c_areas:
            count = 0
            while count < len(c_areas):
                if len(set(area).difference(c_areas[count])) == 1:
                    unique_areas.append(area.union(c_areas[count]))
                count += 1
        
        # If there isn't any changes to make, reattribute the original country areas
        if not unique_areas:
            unique_areas = c_areas

        # Do the math with the minimum number of roads and libraries
        num_roads = 0
        num_cities = 0
        for area in unique_areas:
            num_cities += len(area)
            num_roads += (len(area) - 1) * c_road

        print(unique_areas)
        print(c_areas)
        # Check if there is any isolated city
        isolated_cities = c_lib * (n - num_cities)
        num_librs = c_lib * len(unique_areas) + isolated_cities

        min_cost = num_roads + num_librs
    
    return min_cost

def depthFirstTraverse(town, visited, roads, path):
    visited[town] = True
    for d_town in roads[town]:
        if visited[d_town] == False:
            path.add(d_town)
            depthFirstTraverse(d_town, visited, roads, path)
    # Dead end, if nothing was found to connect to, create a single path

# Complete the roadsAndLibraries function below.
def roadsAndLibraries_imp2(n, c_lib, c_road, cities):
    min_cost = 0
    # Check if the cost of building a library is cheaper than a road
    if c_lib <= c_road:
        min_cost = n * c_lib
    else:
        # Else, prepare the graph algorithm
        roads = {}
        for city in cities:
            # Check for empty city areas, then create, or append:
            x, y = city
            if x not in roads:
                roads[x] = {y}
            else:
                roads[x].add(y)
            if y not in roads:
                roads[y] = {x}
            else:
                roads[y].add(x)

        # Check if there is any isolated city
        towns = set(roads.keys())
        if len(towns) < n:
            isolated_towns = set(range(1, n + 1)).difference(towns)
            isolated_roads = {town: set() for town in isolated_towns}
            roads = {**roads, **isolated_roads}
            towns = towns.union(isolated_towns)
   
        paths = []
        visited = { town: False for town in towns }
        # print(roads)
        while False in visited.values():
            town = [town for town, marked in visited.items() if not marked][0]
            path = {town}
            depthFirstTraverse(town, visited, roads, path)
            paths.append(path)
   
        # Do the math with the minimum number of roads and libraries
        # print(paths)
        num_roads = 0
        num_librs = len(paths) * c_lib
        for path in paths:
            num_roads += (len(path) - 1) * c_road

        min_cost = num_roads + num_librs
    
    return min_cost

def dft(i, count, roads, visited):
    visited[i] = True
    count += 1
    print(count)
    for road in roads[i]:
        if not visited[road]:
            dft(road, count, roads, visited)


# Complete the roadsAndLibraries function below.
def roadsAndLibraries(n, c_lib, c_road, cities):
    i = 1
    cost = 0
    # visited = [False for _ in range(n)]
    roads = {}
    for city in cities:
        # Check for empty city areas, then create, or append:
        x, y = city
        if x not in roads:
            roads[x] = {y}
        else:
            roads[x].add(y)
        if y not in roads:
            roads[y] = {x}
        else:
            roads[y].add(x)

    # Check if there is any isolated city
    towns = set(roads.keys())
    if len(towns) < n:
        isolated_towns = set(range(1, n + 1)).difference(towns)
        isolated_roads = {town: set() for town in isolated_towns}
        roads = {**roads, **isolated_roads}
        towns = towns.union(isolated_towns)

    visited = { town: False for town in towns }

    # paths = []   
    # print(roads)
    # print(visited)
    while i < len(roads):
        if not visited[i]:
            count = 0
            dft(i, count, roads, visited)
            if c_lib > c_road:
                print(count)
                cost += c_lib + (c_road * (count - 1))
            else:
                cost += c_lib * count
        i += 1
    return cost

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