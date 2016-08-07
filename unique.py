#!/usr/bin/python
import os
import sys
import argparse
import logging
import itertools

def swapped_pieces(pieces):
    """
    Create all permutations of the given list of the
    pieces, then return in a list of pieces tuple.

    Keyword arguments:

    pieces -- The pieces dictionary with the quantity of each piece.
    """

    sequence,sequences = [],[]

    # Iterate over the pieces original dict
    for piece,number in pieces.items():
        if number < 1: continue
        times = (("%s " % piece)*number)
        sequence.extend(times.split())

    # Create permutations with itertools.permutations, then return
    sequences.extend(itertools.permutations(sequence))
    return sequences

def main():
    """
    Application main function. It doesn't receive
    arguments by the function, only by the parser.
    """

    # Configures the logging processor for information
    logging.basicConfig(filename='unique.log',level=logging.DEBUG)

    # Configures the argument parser for the input
    parser = argparse.ArgumentParser(description="Find unique configurations of a M x N chessboard.")
    parser.add_argument('-m', type=int, default=0, help="Number of horizontal rows")
    parser.add_argument('-n', type=int, default=0, help="Number of vertical columns")
    parser.add_argument('-K', type=int, default=0, help="King piece quantity, default is 0")
    parser.add_argument('-Q', type=int, default=0, help="Queen piece quantity, default is 0")
    parser.add_argument('-R', type=int, default=0, help="Rook piece quantity, default is 0")
    parser.add_argument('-B', type=int, default=0, help="Bishop piece quantity, default is 0")
    parser.add_argument('-N', type=int, default=0, help="Knight piece quantity, default is 0")
    args = parser.parse_args()
    pieces = vars(args)

    # Verify if there is a valid size for the chessboard
    if args.m < 3 or args.n < 3: sys.exit("Invalid size for the board, it must be 3 x 3 or bigger.")
    m,n = pieces.pop('m'), pieces.pop('n')

    # Verify if there is any piece to test with
    quantity = args.K + args.Q + args.R + args.B + args.N
    if quantity < 2: sys.exit("There isn't enought pieces for combinations, it must be 2 or more.")

    logging.info("Total number of pieces: %d" % quantity)
    logging.info("Relation of pieces for the combination: %s" % pieces)
    logging.info("Chessboard dimensions - Width: %d Height: %d" % (m,n))

    # Generate a list of possible alternative of ordered pieces
    permutations = swapped_pieces(pieces)
    logging.info("Sequence of possible permutations: %s" % permutations)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        # This log will include content written in sys.exit
        logging.exception("Unique has failed with exception")
        logging.error(str(e))
        raise
