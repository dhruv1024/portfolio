#!/bin/python3

import math
import os
import random
import re
import sys

"""def queensAttack(n, k, r_q, c_q, obstacles):
    o, ans = set([(i, j) for i, j in obstacles]), 0
    for i, j in set(product([-1, 0, 1], repeat=2))-{(0, 0)}:
        p = [(r_q+i*k, c_q+j*k) for k in range(1, n+1)]
        ans+=[i not in o and all(0<j<=n for j in i) for i in p].index(0)
    return ans"""

def queensAttack(n, k, r_q, c_q, obstacles):
    # Write your code here
    attackSquares = 0
    obstacles_set = set(tuple(obstacle) for obstacle in obstacles)

    # CalculateStraights
    for i in range(1, r_q):
        if (r_q - i, c_q) in obstacles_set:
            break
        else:
            attackSquares += 1
    for i in range(1, n - r_q + 1):
        if (r_q + i, c_q) in obstacles_set:
            break
        else:
            attackSquares += 1
    for i in range(1, c_q):
        if (r_q, c_q - i) in obstacles_set:
            break
        else:
            attackSquares += 1
    for i in range(1, n - c_q + 1):
        if (r_q, c_q + i) in obstacles_set:
            break
        else:
            attackSquares += 1

    # FirstQuadPoints
    for i in range(1, min(r_q - 1, c_q - 1) + 1):
        if (r_q - i, c_q - i) in obstacles_set:
            break
        else:
            attackSquares += 1
    # SecondQuadPoints
    for i in range(1, min(r_q - 1, n - c_q) + 1):
        if (r_q + i, c_q - i) in obstacles_set:
            break
        else:
            attackSquares += 1
    # ThirdQuadPoints
    for i in range(1, min(n - r_q, n - c_q) + 1):
        if (r_q + i, c_q + i) in obstacles_set:
            break
        else:
            attackSquares += 1
    # FourthQuadPoints
    for i in range(1, min(n - r_q, c_q - 1) + 1):
        if (r_q - i, c_q + i) in obstacles_set:
            break
        else:
            attackSquares += 1
    
    return attackSquares

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        n, k = map(int, file.readline().split())
        r_q, c_q = map(int, file.readline().split())
        obstacles = [list(map(int, file.readline().split())) for _ in range(k)]

    # Call the function
    result = queensAttack(n, k, r_q, c_q, obstacles)

    # Write the result to an output file
    with open('output_file.txt', 'w') as file:
        file.write(str(result) + '\n')
