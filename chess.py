#!/usr/bin/python

import argparse
import logging
import sys

logging.basicConfig(filename='chess.log',level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Find unique configurations of a MxN chess')
parser.add_argument('-n',help='Vertical columns of squares')
parser.add_argument('-m',help='Horizontal rows of squares')
args = vars(parser.parse_args())

K = 0
Q = 0
B = 0
R = 0
N = 0

def main():
    if not args['m'] and not args['n']:
        logging.error('You must specify the number of squares of the chessboard.')
        sys.exit('Exitting the program.')
    chess_m = args['m']
    chess_n = args['n']
    #print("Hello World!")

if __name__ == "__main__": main()
