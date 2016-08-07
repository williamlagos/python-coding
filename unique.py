#!/usr/bin/python
#
# Unique Combinations python app
# This application find the unique combinations of X pieces on a M x N chessboard
#
# 0 - free to use
# 1 - threat zone
# Unicode - piece placed
#
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

import os
import sys
import logging
import argparse
import itertools

movements = {
    # 'P': (0, 1, 2, 3, 4, 5, 6, 7),
    # 'P': (N, E, S, W,NE,SE,SW,NW),
    'K':(1,1,1,1,1,1,1,1),
    'Q':(2,2,2,2,2,2,2,2),
    'R':(2,2,2,2,0,0,0,0),
    'B':(0,0,0,0,2,2,2,2),
    'N':(0,0,0,0,0,0,0,0),
}

def verify_adjacents(t,board,x,y):
    """
    Verify the adjacencies of the square that the
    piece will be put.

    Keyword arguments:

    t -- Type of the chess piece
    board -- The chessboard matrix with integer codes
    x -- X position on the chessboard to put the piece
    y -- Y position on the chessboard to put the piece
    """

    both = px = py = d = 0
    max_x = max_y = len(board)
    available,adjacencies,available_directions = [],[],[]
    # It doesn't need to verify the upper or down directions if we are on extremity
    if y == 0: available = [3,6,2,5,1]
    elif y == max_y: available = [3,7,0,4,1]
    # If the square is in the middle, all the vertical adjacencies will be checked
    else:
        available = [3,6,7,0,2,4,5,1]
        both += 1

    # Verify if the square isn't on the horizontal extremities
    if x == 0: available_directions = available[2 + both:]
    elif x == max_x: available_directions = available[:-2 - both]

    squares = (1,1,1,1)
    directions = movements[t]

    # Special adjacencies for the knight movement
    if sum(directions) == 0:
        # Special extremities for the knight
        px = py = 0
        w_knight = x >= 2
        n_knight = y >= 2
        e_knight = (max_x - x) >= 2
        s_knight = (max_y - y) >= 2

        has_north = 0 in available_directions
        has_south = 2 in available_directions
        has_west = 3 in available_directions
        has_east = 1 in available_directions

        # North direction adjacencies
        if w_knight and has_north:
            px = x - 2; py = y - 1
            if board[px][py] > 0: return []
            else: adjacencies.append((px,py))
        if n_knight and has_west:
            px = x - 1; py = y - 2
            if board[x-1][y-2] > 0: return []
            else: adjacencies.append((px,py))
        if w_knight and has_south:
            px = x - 2; py = y + 1
            if board[x-2][y+1] > 0: return []
            else: adjacencies.append((px,py))
        if n_knight and has_east:
            px = x + 1; py = y - 2
            if board[px][py] > 0: return []
            else: adjacencies.append((px,py))

        # South directions adjacencies
        if s_knight and has_west:
            px = x - 1; py = y + 2
            if board[px][py] > 0: return []
            else: adjacencies.append((px,py))
        if e_knight and has_south:
            px = x + 2; py = y + 1
            if board[px][py] > 0: return []
            else: adjacencies.append((px,py))
        if s_knight and has_east:
            px = x + 1; py = y + 2
            if board[px][py] > 0: return []
            else: adjacencies.append((px,py))
        if e_knight and has_north:
            px = x + 2; py = y - 1
            if board[px][py] > 0: return []
            else: adjacencies.append((px,py))

    # Iterate over the available directions and verify if it's viable to put the piece in this position
    while d < len(available_directions):
        if directions[d] == 0: return
        # Verify if the directions of this piece are just one square per time or the entire row/column
        if directions[d] > 1: squares = y - 1, x - 1, max_y - y, max_x - x
        # North direction adjacencies
        if available_directions[d] == 0:
            for s in range(squares[0]):
                py = y; px = x - (1 * s)
                if board[px][py] > 0: return []
                else: adjacencies.append((px,py))
        # East direction adjacencies
        elif available_directions[d] == 1:
            for s in range(squares[1]):
                px = x; py = y + (1 * s)
                if board[px][py] > 0: return []
                else: adjacencies.append((px,py))
        # South direction adjacencies
        elif available_directions[d] == 2:
            for s in range(squares[2]):
                py = y; px = x + (1 * s)
                if board[px][py] > 0: return []
                else: adjacencies.append((px,py))
        # West direction adjacencies
        elif available_directions[d] == 3:
            for s in range(squares[3]):
                px = x; py = y - (1 * s)
                if board[px][py] > 0: return []
                else: adjacencies.append((px,py))
        # North-east direction adjacencies
        elif available_directions[d] == 4:
            for s1,s2 in zip(range(squares[0]),range(squares[1])):
                px = x - (1 * s1); py = y + (1 * s2)
                if board[px][py] > 0: return []
                else: adjacencies.append((px,py))
        # South-east direction adjacencies
        elif available_directions[d] == 5:
            for s1,s2 in zip(range(squares[2]),range(squares[1])):
                px = x + (1 * s1); py = y + (1 * s2)
                if board[px][py] > 0: return []
                else: adjacencies.append((px,py))
        # South-west direction adjacencies
        elif available_directions[d] == 6:
            for s1,s2 in zip(range(squares[2]),range(squares[3])):
                px = x + (1 * s1); py = y - (1 * s2)
                if board[px][py] > 0: return []
                else: adjacencies.append((px,py))
        # North-west direction adjacencies
        elif available_directions[d] == 7:
            for s1,s2 in zip(range(squares[2]),range(squares[3])):
                px = x - (1 * s1); py = y - (1 * s2)
                if board[px][py] > 0: return []
                else: adjacencies.append((px,py))
        d += 1
    return adjacencies


def unique_configuration(sequence,board):
    """
    Search for a unique configuration for a given
    sequence of pieces on a chessboard with given
    dimensions.

    Keyword arguments:

    sequence -- A permutated sequence of pieces
    board -- The chessboard matrix with integer codes
    """

    adjacencies = []
    # Verify if there is more piece to put in the board
    if len(sequence) > 0:
        p = sequence[0]
        for y,row in enumerate(board):
            for x,square in enumerate(row):
                # Verify if the position has threat or piece placed
                if square != 0: continue
                # Verify if the adjacencies of the position are available
                adjacencies = verify_adjacents(p,board,x,y)
                if not adjacencies: continue
                # print(adjacencies)

    # If not, the function returns its recursive call
    else: return
    unique_configuration(sequence[1:],board)


def possible_ordered_sequences(pieces):
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

    # Create permutations with itertools.permutations, then return a set of it
    sequences.extend(itertools.permutations(sequence))
    return set(sequences)

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
    permutations = possible_ordered_sequences(pieces)
    logging.info("Sequence of possible permutations: %s" % permutations)

    # Generate the board matrix with zeros and call recursive function for unique configurations
    board = [[0] * m for i in itertools.repeat(None, m)]
    for sequence in permutations: unique_configuration(sequence,board)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        # This log will include content written in sys.exit
        logging.exception("Unique has failed with exception")
        logging.error(str(e))
        raise
