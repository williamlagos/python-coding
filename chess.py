#!/usr/bin/python
#
# Unique Combinations python app
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

""" Finds the unique combinations of X pieces on a M x N chessboard """

import sys
import timeit
import logging
import argparse
import board

def main():
    """

    Application main function. It doesn't receive
    arguments by the function, only by the parser.

    """

    # Configures the logging processor for information
    logging.basicConfig(filename='chess.log', level=logging.INFO, format='%(asctime)s %(message)s')

    # Configures the argument parser for the input
    parser = argparse.ArgumentParser(
        description="Find unique configurations of a M x N chessboard.")
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
    if args.m < 3 or args.n < 3:
        sys.exit("Invalid size for the board, it must be 3 x 3 or bigger.")
    row, col = pieces.pop('m'), pieces.pop('n')

    # Verify if there is any piece to test with
    quantity = args.K + args.Q + args.R + args.B + args.N
    if quantity < 2:
        sys.exit("There isn't enought pieces for combinations, it must be 2 or more.")

    logging.info("Total number of pieces: %d", quantity)
    logging.info("Relation of pieces for the combination: %s", pieces)
    logging.info("Chessboard dimensions - Rows: %d Columns: %d", row, col)

    start = timeit.default_timer()

    # configurations = []
    configurations = 0
    # Generate a list of possible alternative of ordered pieces
    permutations = board.possible_ordered_sequences(pieces)
    logging.info("Sequence of possible permutations: %s", permutations)

    # Generate the board matrix with zeros and call function for unique configurations
    for seq in permutations:
        sequence = board.piece_sequence(seq)
        for y in range(row):
            for x in range(col):
                config = board.Board(col, row)
                if config.combinations(sequence, (x, y)):
                    configurations += 1
                    print(config)
                    # configurations.append(config)
    # for cfg in configurations:
    #     print(cfg)

    elapsed = timeit.default_timer() - start
    print("Number of permutations: %d" % len(permutations))
    print("Total Unique Amount: %d" % configurations)
    print("Time elapsed %ss" %elapsed)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as err:
        # This log will include content written in sys.exit
        # logging.exception()
        logging.error(str(err))
        raise
