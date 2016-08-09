#!/usr/bin/python
#
# Unique Combinations python app
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

""" Unique module with main functions """

import logging
import itertools
import pieces

# 0 - free to use
# 1 - threat zone
# Unicode - piece placed
FREE = 0
THREAT = 1

def prepare_boundaries(board, pos_x, pos_y):
    """

    Verify the boundaries of the square that the
    piece will be put.

    Keyword arguments:

    board -- The chessboard matrix with integer codes
    pos_x -- X position on the chessboard to put the piece
    pos_y -- Y position on the chessboard to put the piece

    """

    ext_x, ext_y = (len(board[0]) - 1, len(board) - 1)

    # Boundaries relation
    # N  E  S  W  NE SE SW NW
    # 0  1  2  3  4  5  6  7
    boundaries = [0, 1, 2, 3, 4, 5, 6, 7]
    # It doesn't need to verify the upper or down directions if we are on extremity

    if pos_x == 0:
        # Corner upper left
        if pos_y == 0:
            boundaries = [1, 2, 5]
        # Corner down left
        elif pos_y == ext_y:
            boundaries = [0, 1, 4]
        # Between corners left
        else:
            boundaries = [0, 1, 2, 4, 5]
    elif pos_x == ext_x:
        # Corner upper right
        if pos_y == 0:
            boundaries = [2, 3, 6]
        # Corner down right
        elif pos_x == ext_x:
            boundaries = [0, 3, 7]
        # Between corners right
        else:
            boundaries = [0, 2, 3, 6, 7]
    elif pos_y == 0:
        # Upper between corners
        boundaries = [1, 2, 3, 5, 6]
    elif pos_y == ext_y:
        # Down between corners
        boundaries = [0, 1, 3, 4, 7]

    # If the square is in the middle, all the vertical adjacencies will be checked
    logging.debug("Verified existing boundaries on board: %s", boundaries)

    return boundaries

def put_piece(piece, board, pos_x, pos_y):
    """

    Put the given piece in the board with its adjacencies included.

    Keyword arguments:

    piece -- Piece object that will be inserted
    board -- Main matrix chessboard to be manipulated
    x -- X position of the given piece
    y -- Y position of the given piece

    """
    logging.debug("Board before insertion of %s in (%d, %d): %s", piece.letter, pos_x, pos_y, board)
    # Put the piece with the unicode representation on board
    board[pos_x][pos_y] = ord(str(piece))

    logging.debug("List of adjacencies of %s for (%d, %d): %s",
                  piece.letter, pos_x, pos_y, piece.adjacencies)
    # Insert all the adjacencies related to the piece
    for _, adj in piece.adjacencies.items():
        adj_x, adj_y = adj
        board[adj_x][adj_y] = THREAT
    logging.debug("Board after insertion of %s in (%d, %d): %s", piece.letter, pos_x, pos_y, board)

def unique_configuration(sequence, board):
    """

    Search for a unique configuration for a given
    sequence of pieces on a chessboard with given
    dimensions.

    Keyword arguments:

    sequence -- A permutated sequence of pieces
    board -- The chessboard matrix with integer codes

    """

    pieces_placed = 0
    # Verify if there is more piece to put in the board
    logging.debug("Working with sequence %s", sequence)
    chess_pieces = pieces.PieceFactory.generate_pieces(sequence)
    for piece in chess_pieces:
        for pos_y, row in enumerate(board):
            for pos_x, square in enumerate(row):
                # Verify if the position has threat or piece placed
                logging.debug("Starting to check piece %s in position (%d,%d)", piece, pos_x, pos_y)
                if square != 0:
                    continue
                logging.debug("Preparing boundaries for the piece %s", piece)
                boundaries = prepare_boundaries(board, pos_x, pos_y)
                piece.prepare_adj(board, pos_x, pos_y)
                # Verify if the adjacencies of the position are available
                if piece.check_adj(boundaries, board, pos_x, pos_y):
                    continue
                logging.debug("Putting piece %s on board", piece)
                put_piece(piece, board, pos_x, pos_y)
                pieces_placed += 1
    # Verify if all the pieces were placed on chessboard
    return pieces_placed == len(sequence)


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
