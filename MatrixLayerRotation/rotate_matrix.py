#!/bin/python

import math
import os
import random
import re
import sys

global numrows, numcols, numloops
global matrix, turns
global range_numrows, range_numcols, range_numloops
global loop_indices, len_loop_indices
debug = False

# Complete the matrixRotation function below.
def matrixRotation(m, r):
    global matrix, turns
    matrix = m
    turns = r
    global numrows, numcols, numloops
    numrows = len(matrix)
    numcols = len(matrix[0])
    numloops = int(min(round(numrows/2.0,0), round(numcols/2.0,0)))
    global range_numrows, range_numcols, range_numloops
    range_numrows = range(numrows)
    range_numcols = range(numcols)
    range_numloops = range(numloops)
    # list of indices in each CCW loop starting top-right corner
	# ('0_3', '0_2', '0_1', '0_0', '1_0', '2_0',..., '1_3'),
	# ('1_2', '1_1', '2_1', '2_2')

    def get_loop_indices(loop=-1):
        global loop_indices, len_loop_indices
        if loop < 0:
            loop_indices = [None] * numloops
            len_loop_indices = [None] * numloops
            for loop in range_numloops:
                get_loop_indices(loop)
            if debug:
                for a in loop_indices:
                    print a
            return
        loop_indices[loop] = []
        # top: row=loop, col=numcols-1-loop to loop
        data = []
        for col in range(numcols-1-loop, loop-1, -1):
            data.append("{:d}_{:d}".format(loop, col))
        if debug: print_loop(loop, 'TOP   ', data)
        loop_indices[loop].extend(data)
        # left:  row=loop+1 to numrows-1-loop-1, col=loop
        data = []
        for row in range(loop+1, numrows-1-loop-1+1):
            data.append("{:d}_{:d}".format(row, loop))
        if debug: print_loop(loop, 'LEFT  ', data)
        loop_indices[loop].extend(data)
        # bottom: row=numrows-1-loop, col=loop to numcols-1-loop
        data = []
        for col in range(loop, numcols-1-loop+1):
            data.append("{:d}_{:d}".format(numrows-1-loop, col))
        if debug: print_loop(loop, 'BOTTOM', data)
        loop_indices[loop].extend(data)
        # right: row=numrows-1-loop-1 to loop+1, col=numcols-1-loop
        data = []
        for row in range(numrows-1-loop-1, loop+1-1, -1):
            data.append("{:d}_{:d}".format(row, numcols-1-loop))
        if debug: print_loop(loop, 'RIGHT ', data)
        loop_indices[loop].extend(data)
        len_loop_indices[loop] = len(loop_indices[loop] )

    def is_off_loop(loop, i, j):
        return not "{:d}_{:d}".format(i, j) in loop_indices[loop]



    def turn(loop, i, j):  # return new location after the CCW turn
        ij = "{:d}_{:d}".format(i, j)
        l = len_loop_indices[loop]
        k = loop_indices[loop].index(ij)    # index of ij in loop list
        m = k + turns                       # new position after turns
        m = m % l   # actual position
        return map(int, loop_indices[loop][m].split('_')) 

    def print_matrix(m=None):
        if not m: m = matrix        
        for i in range_numrows:
            s = ""
            for j in range_numcols:
                v = m[i][j]
                if j > 0: s += ' '
                if not v: s += "None"
                else:     s += str(v)
            if i < numrows - 1: s += '\n'
            sys.stdout.write(s)

    def print_loop(loop, sidename, data):
        sys.stdout.write("Loop: {:>3d} Side: {} - Data: ".format(loop, sidename))
        s = ""
        for a in data: s += " " + a
        sys.stdout.write(s + '\n')

    def init_matrix():
        m = [None]*numrows
        for i in range_numrows:
            m[i] = [None]*numcols
        return m

    def copy_matrix(m=None):
        if not m: m = matrix
        m2 = [None]*numrows
        for i in range_numrows:
            m2[i] = m[i][:]  # copy
        return m2

    # -------------- main ------------------------------
    # for each turn
    #  for each loop in matrix
    #    for each element in matrix that is on the loop
    #      shift CCW and store in scratch matrix
    #  swap matrix
    get_loop_indices()
    matrix1 = init_matrix()
    if debug: 
        print_matrix(matrix)
        print "-------------------"
    for loop in range_numloops:
        for i in range_numrows:
            for j in range_numcols:
                if is_off_loop(loop, i, j): continue
                i1, j1 = turn(loop, i, j)
                matrix1[i1][j1] = matrix[i][j]
    print_matrix(matrix1)

if __name__ == '__main__':
    mnr = raw_input().rstrip().split()

    m = int(mnr[0])

    n = int(mnr[1])

    r = int(mnr[2])

    matrix = []

    for _ in xrange(m):
        matrix.append(map(int, raw_input().rstrip().split()))

    matrixRotation(matrix, r)
