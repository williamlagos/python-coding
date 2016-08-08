#!/usr/bin/python
#
# Unique Combinations python app
# This application find the unique combinations of X pieces on a M x N chessboard
#
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

import os
import sys
import json
import logging
import argparse
import itertools

# 0,1,2,3,4,5,6,7 are constants to North,East,South,West,
# Northeast,Southeast,South-west and Northwest, respectively.

N = 0
E = 1
S = 2
W = 3
NE = 4
SE = 5
SW = 6
NW = 7

# 0 - free to use
# 1 - threat zone
# Unicode - piece placed

FREE = 0
THREAT = 1

def check_nzone(direction,adjacencies,board,x,y):
    """
    Verify the threat zone for knight special squares
    for a given piece and a given direction (N,E,S,W,NE,SE,SW,NW).

    Keyword arguments:

    direction -- Direction of the check (N,E,S,W,NE,SE,SW,NW)
    adjacencies -- List with available adjacencies
    board -- Matrix main chessboard
    x -- X position of the piece
    y -- Y position of the piece
    """

    px = py = 0
    logging.debug("Checking knight zone on direction %s in position (%d,%d)" % (direction,x,y))
    # North knight direction
    if direction is N:
        px = x - 2; py = y - 1
    # East knight direction
    elif direction is E:
        px = x + 1; py = y - 2
    # South knight direction
    elif direction is S:
        px = x - 2; py = y + 1
    # West knight direction
    elif direction is W:
        px = x - 1; py = y - 2
    # Northeast knight direction
    elif direction is NE:
        px = x + 1; py = y + 2
    # Southeast knight direction
    elif direction is SE:
        px = x + 2; py = y + 1
    # Southwest knight direction
    elif direction is SW:
        px = x - 1; py = y + 2
    # Northwest knight direction
    elif direction is NW:
        px = x + 2; py = y - 1
    if board[px][py] != FREE: return True
    else:
        adjacencies.append((px,py))
        logging.debug("Added (%d,%d) as a valid adjacency for the piece in (%d,%d)" % (px,py,x,y))
        return False

def check_dzone(direction,adjacencies,squares1,squares2,board,x,y):
    """
    Verify the threat zone for diagonal 1 - n squares
    for a given piece and a given direction (N,E,S,W).

    Keyword arguments:

    direction -- Direction of the check (N,E,S,W)
    adjacencies -- List with available adjacencies
    squares1 -- Number of squares to be verified on X coordinate
    squares2 -- Number of squares to be verified on Y coordinate
    board -- Matrix main chessboard
    x -- X position of the piece
    y -- Y position of the piece
    """

    px = py = 0
    logging.debug("Checking diagonal zone on direction %s in position (%d,%d)" % (direction,x,y))
    logging.debug("Number of squares to be checked: X:%d Y:%d" % (squares1,squares2))
    # if squares is 1, it'll iterate just one time (K movement)
    for s1,s2 in zip(range(squares1),range(squares2)):
        # Northeast direction
        if direction is NE:
            px = x - (1 * s1)
            py = y + (1 * s2)
        # Southeast direction
        elif direction is SE:
            px = x + (1 * s1)
            py = y + (1 * s2)
        # South-west direction
        elif direction is SW:
            px = x + (1 * s1)
            py = y - (1 * s2)
        # Northwest direction
        elif direction is NW:
            px = x - (1 * s1)
            py = y - (1 * s2)
        if board[px][py] != FREE: return True
        else:
            adjacencies.append((px,py))
            logging.debug("Added (%d,%d) as a valid adjacency for the piece in (%d,%d)" % (px,py,x,y))
    return False

def check_zone(direction,adjacencies,squares,board,x,y):
    """
    Verify the threat zone for horizontal and vertical 1 - n squares
    for a given piece and a given direction (N,E,S,W).

    Keyword arguments:

    direction -- Direction of the check (N,E,S,W)
    adjacencies -- List with available adjacencies
    squares -- Number of squares to be verified
    board -- Matrix main chessboard
    x -- X position of the piece
    y -- Y position of the piece
    """

    px = py = 0
    logging.debug("Checking zone on direction %s in position (%d,%d)" % (direction,x,y))
    logging.debug("Number of squares to be checked: %d" % (squares))
    # if squares is 1, it'll iterate just one time (K movement)
    for s in range(squares):
        # North direction
        if direction is N:
            px = x - (1 * s); py = y
        # East direction
        elif direction is E:
            px = x; py = y + (1 * s)
        # South direction
        elif direction is S:
            px = x + (1 * s); py = y
        # West direction
        elif direction is W:
            px = x; py = y - (1 * s)
        if board[px][py] != FREE: return True
        else:
            adjacencies.append((px,py))
            logging.debug("Added (%d,%d) as a valid adjacency for the piece in (%d,%d)" % (px,py,x,y))
    return False

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
    adj,zone,available_zone = [],[],[]
    # It doesn't need to verify the upper or down directions if we are on extremity
    if y == 0: zone = [3,6,2,5,1]
    elif y == max_y: zone = [3,7,0,4,1]
    # If the square is in the middle, all the vertical adjacencies will be checked
    else:
        zone = [3,6,7,0,2,4,5,1]
        both += 1

    # Verify if the square isn't on the horizontal extremities
    if x == 0: available_zone = zone[2 + both:]
    elif x == max_x: available_zone = zone[:-2 - both]
    logging.debug("Verified existing limits on board and possible directions: %s" % available_zone)

    # A fixed dict with the movements of each piece are stored in a file called unique.json.
    f = open('unique.json','r')
    movements = json.load(f)
    directions = movements[t]
    logging.debug("Checked possible movements of piece of type %s: %s" % (t,directions))

    # Special adjacencies for the knight movement
    if sum(directions) == 0:
        logging.debug("Knight type movement detected, proceding to special limits")
        # North direction adjacencies with special extemities
        if N in available_zone and x >= 2:
            if check_nzone(N,adj,board,x,y): return []
        if S in available_zone and x >= 2:
            if check_nzone(S,adj,board,x,y): return []
        if W in available_zone and y >= 2:
            if check_nzone(W,adj,board,x,y): return []
        if E in available_zone and y >= 2:
            if check_nzone(E,adj,board,x,y): return []

        # South directions adjacencies with special extremities
        if W in available_zone and (max_y - y) >= 2:
            if check_nzone(SW,adj,board,x,y): return []
        if E in available_zone and (max_y - y) >= 2:
            if check_nzone(NE,adj,board,x,y): return []
        if S in available_zone and (max_x - x) >= 2:
            if check_nzone(SE,adj,board,x,y): return []
        if N in available_zone and (max_x - x) >= 2:
            if check_nzone(NW,adj,board,x,y): return []

    # Iterate over the available directions and verify if it's viable to put the piece in this position
    sq = (1,1,1,1)
    for d,available in enumerate(available_zone):
        logging.debug("Normal type movement detected, proceding to normal limits")
        # Verify if this piece can go this direction
        if directions[d] == 0: return
        # Verify if the directions of this piece are just one square per time or the entire row/column
        if directions[d] > 1: sq = y - 1, x - 1, max_y - y, max_x - x
        else: logging.debug("King type movement detected, proceding to unary limits")
        # Verify all the possible direction adjacencies
        if available is N:
            if check_zone(N,adj,sq[0],board,x,y): return []
        elif available is E:
            if check_zone(E,adj,sq[1],board,x,y): return []
        elif available is S:
            if check_zone(S,adj,sq[2],board,x,y): return []
        elif available is W:
            if check_zone(W,adj,sq[3],board,x,y): return []
        elif available is NE:
            if check_dzone(NE,adj,sq[0],sq[1],board,x,y): return []
        elif available is SE:
            if check_dzone(SE,adj,sq[2],sq[1],board,x,y): return []
        elif available is SW:
            if check_dzone(SW,adj,sq[2],sq[3],board,x,y): return []
        elif available is NW:
            if check_dzone(NW,adj,sq[2],sq[3],board,x,y): return []

    # If the function didn't return until this point, it's possible to put the piece in x,y coordinate
    logging.debug("All adjancencies are valid, proceding to deliver to unique_configuration()")
    return adj

def put_piece(adjacencies,p,board,x,y):
    """
    Put the given piece in the board with its adjacencies included.

    Keyword arguments:

    adjacencies -- List of adjacencies of the piece
    p -- The letter of the piece that will be inserted
    board -- Main matrix chessboard to be manipulated
    x -- X position of the given piece
    y -- Y position of the given piece
    """
    logging.debug("Board before insertion of %s in (%d,%d): %s" % (p,x,y,board))
    # Put the piece with the unicode representation on board
    board[x][y] = ord(p)

    logging.debug("List of adjacencies of %s for (%d,%d): %s" % (p,x,y,adjacencies))
    # Insert all the adjacencies related to the piece
    for x,y in adjacencies: board[x][y] = THREAT
    logging.debug("Board after insertion of %s in (%d,%d): %s" % (p,x,y,board))

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
                logging.debug("Putting piece %s on board" % p)
                put_piece(adjacencies,p,board,x,y)

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

    # print(board)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        # This log will include content written in sys.exit
        logging.exception("Unique has failed with exception")
        logging.error(str(e))
        raise
