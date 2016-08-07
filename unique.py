#!/usr/bin/python
import sys
import argparse
import logging

def main():
    """
    Application main function. It doesn't receive
    arguments by the function, only by the parser.
    """

    # Configures the logging processor for information
    logging.basicConfig(filename='unique.log',level=logging.DEBUG)

    # Configures the argument parser for the input
    parser = argparse.ArgumentParser(description='Find unique configurations of a M x N chessboard.')
    parser.add_argument('-m', type=int, default=0, help='Number of horizontal rows')
    parser.add_argument('-n', type=int, default=0, help='Number of vertical columns')
    parser.add_argument('-K', type=int, default=0, help='King piece quantity, default is 0')
    parser.add_argument('-Q', type=int, default=0, help='Queen piece quantity, default is 0')
    parser.add_argument('-R', type=int, default=0, help='Rook piece quantity, default is 0')
    parser.add_argument('-B', type=int, default=0, help='Bishop piece quantity, default is 0')
    parser.add_argument('-N', type=int, default=0, help='Knight piece quantity, default is 0')
    args = parser.parse_args()
    pieces = vars(args)

    # Verify if there is a valid size for the chessboard
    if args.m < 3 or args.n < 3: sys.exit(1)
    m,n = pieces.pop('m'), pieces.pop('n')

    # Verify if there is any piece to test with
    quantity = args.K + args.Q + args.R + args.B + args.N
    if quantity < 2: sys.exit(1)

    logging.info("Total number of pieces: %d" % quantity)
    logging.info("Relation of pieces for the combination: %s" % pieces)
    logging.info("Chessboard dimensions - Width: %d Height: %d" % (m,n))

if __name__ == "__main__":
    main()
