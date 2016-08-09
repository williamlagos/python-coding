#!/usr/bin/python
#
# Unique Combinations python app
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

""" Unique module with main functions """

import logging
import itertools
# import pieces

# Position tuple codes
X = 0
Y = 1

# 0 - free to use
# 1 - threat zone
# Unicode - piece placed
FREE = 0
THREAT = 1

def verify_boundaries(typ, board, pos_x, pos_y):
    """

    Verify the boundaries of the square that the
    piece will be put.

    Keyword arguments:

    typ -- Type of the chess piece
    board -- The chessboard matrix with integer codes
    pos_x -- X position on the chessboard to put the piece
    pos_y -- Y position on the chessboard to put the piece

    """

    logging.debug("Verifiying boundaries for the piece %s", typ)
    both = 0
    ext = (len(board[0]), len(board))
    adj, zone, available_zone = [], [], []
    # It doesn't need to verify the upper or down directions if we are on extremity
    if pos_y == 0:
        zone = [3, 6, 2, 5, 1]
    elif pos_y == ext[Y]:
        zone = [3, 7, 0, 4, 1]
    # If the square is in the middle, all the vertical adjacencies will be checked
    else:
        zone = [3, 6, 7, 0, 2, 4, 5, 1]
        both += 1

    # Verify if the square isn't on the horizontal extremities
    if pos_x == 0:
        available_zone = zone[2 + both:]
    elif pos_x == ext[X]:
        available_zone = zone[:-2 - both]
    else:
        available_zone = zone
    logging.debug("Verified existing boundaries on board: %s", available_zone)

    # A fixed dict with the movements of each piece are stored in a file called movements.json.
    # cfg = open('movements.json', 'r')
    # movements = json.load(cfg)
    # logging.debug("Checked possible movements of piece of type %s: %s", typ, movements[typ])
    #
    # # Special adjacencies for the knight movement
    # if sum(movements[typ]) == 0:
    #     logging.info("Knight type movement detected, proceding to special limits")
    #     if pieces.check_knight_adjacencies(available_zone, adj, board, (pos_x, pos_y)):
    #         return []
    # else:
    #     logging.info("Normal type movement detected, proceding to normal limits")
    #     if pieces.check_adjacencies(available_zone, movements[typ], adj, board, (pos_x, pos_y)):
    #         return []
    # If the function didn't return until this point,
    # it's possible to put the piece in x, y coordinate
    logging.debug("Valid adjacencies found: %s", adj)
    logging.info("All adjacencies are valid, proceding to deliver it")
    return adj

def put_piece(adjacencies, piece, board, pos_x, pos_y):
    """

    Put the given piece in the board with its adjacencies included.

    Keyword arguments:

    adjacencies -- List of adjacencies of the piece
    piece -- The letter of the piece that will be inserted
    board -- Main matrix chessboard to be manipulated
    x -- X position of the given piece
    y -- Y position of the given piece

    """
    logging.debug("Board before insertion of %s in (%d, %d): %s", piece, pos_x, pos_y, board)
    # Put the piece with the unicode representation on board
    board[pos_x][pos_y] = ord(piece)

    logging.debug("List of adjacencies of %s for (%d, %d): %s", piece, pos_x, pos_y, adjacencies)
    # Insert all the adjacencies related to the piece
    for pos_x, pos_y in adjacencies:
        board[pos_x][pos_y] = THREAT
    logging.debug("Board after insertion of %s in (%d, %d): %s", piece, pos_x, pos_y, board)

def unique_configuration(sequence, board):
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
    logging.debug("Working with sequence %s", sequence)
    for piece in sequence:
        for pos_y, row in enumerate(board):
            for pos_x, square in enumerate(row):
                # Verify if the position has threat or piece placed
                if square != 0:
                    continue
                # Verify if the adjacencies of the position are available
                adjacencies = verify_boundaries(piece, board, pos_x, pos_y)
                if not adjacencies:
                    continue
                logging.debug("Putting piece %s on board", piece)
                put_piece(adjacencies, piece, board, pos_x, pos_y)

def possible_ordered_sequences(piece_dict):
    """

    Create all permutations of the given list of the
    pieces, then return in a list of pieces tuple.

    Keyword arguments:

    piece_dict -- The pieces dictionary with the quantity of each piece.

    """

    sequence, sequences = [], []

    # Iterate over the pieces original dict
    for piece, number in piece_dict.items():
        if number < 1:
            continue
        times = (("%s " % piece)*number)
        sequence.extend(times.split())

    # Create permutations with itertools.permutations, then return a set of it
    sequences.extend(itertools.permutations(sequence))
    return set(sequences)