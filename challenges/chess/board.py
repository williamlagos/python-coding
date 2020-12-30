#!/usr/bin/python
#
# Unique Combinations python app
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

""" Unique module with main functions """

import logging
import itertools
import pieces

boards = []
# 0 - free to use
# 1 - threat zone
# Unicode - piece placed
FREE, THREAT = [x for x in range(2)]

def insert_piece(board, piece, pos_x, pos_y):
    """

    Put the given piece in the board with its adjacencies included.

    Keyword arguments:

    piece -- Piece object that will be inserted
    board -- Main matrix chessboard to be manipulated
    x -- X position of the given piece
    y -- Y position of the given piece

    """
    logging.debug("Board before insertion of %s in (%d, %d): %s",
                  piece.letter, pos_x, pos_y, board)
    # Put the piece with the unicode representation on board
    board[pos_y][pos_x] = ord(str(piece))

    logging.debug("List of adjacencies of %s for (%d, %d): %s",
                  piece.letter, pos_x, pos_y, piece.adjacencies)
    # Insert all the adjacencies related to the piece
    for _, adj in piece.adjacencies.items():
        if isinstance(adj, list):
            for adj_t in adj:
                adj_x, adj_y = adj_t
                board[adj_y][adj_x] = THREAT
        else:
            adj_x, adj_y = adj
            board[adj_y][adj_x] = THREAT
    logging.debug("Board after insertion of %s in (%d, %d): %s",
                  piece.letter, pos_x, pos_y, board)

def combinations(board, sequence, position, verbose):
    """

    Search for a unique configuration for a given
    sequence of pieces on a chessboard with given
    dimensions. Recursive call for board matrix
    using recursive algorithm.

    Keyword arguments:
    board -- The chessboard matrix with integer codes
    sequence -- A permutated sequence of pieces
    position -- The position tuple (X,Y) of matrix to be started

    """
    # Verify if all pieces were placed
    if not sequence:
        boards.append(board)
        if verbose:
            print(board_str(board))
        del board[:]
        del board
        return True

    piece = sequence[0]
    col, row = position
    while row < len(board):
        while col < len(board[0]):
            # Verify if the position is available for insertion
            if board[row][col] == 0:
                boundaries = prepare_boundaries(board, col, row)
                # Verify if the adjacencies of the position are available
                if not piece.check_adj(boundaries, board, col, row):
                    # Prepares for a new try with the remaining pieces
                    new_board = [r[:] for r in board]
                    insert_piece(new_board, piece, col, row)
                    combinations(new_board, sequence[1:], (col, row), verbose)
                    del new_board[:]
                    del new_board
            col += 1
        row += 1
        col = 0

    # If there any pieces that weren't placed, return false
    if sequence:
        del sequence[:]
        del sequence
        return False

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
        elif pos_y == ext_y:
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

def board_str(board):
    """

    String representation of the board. Unicode character for the piece,
    1 for threat zone and 0 for empty zone.

    """
    mat = ''
    for row in board:
        for squ in row:
            if squ > 1:
                mat += '%s ' % chr(squ)
            else:
                mat += '. '
        mat += '\n'
    return mat

def basic_sequence(piece_dict):
    """

    Create a basic sequence with the given pieces.

    Keyword arguments:

    piece_dict -- The pieces dictionary with the quantity of each piece.

    """

    sequence = []
    # Iterate over the pieces original dict
    for piece, number in piece_dict.items():
        if number < 1:
            continue
        times = (("%s " % piece)*number)
        sequence.extend(times.split())
    return sequence

def unique(iterable):
    """ Get a unique sequence """
    seen = set()
    for psx in iterable:
        if psx in seen:
            continue
        seen.add(psx)
        yield psx

def possible_ordered_sequences(piece_dict):
    """

    Create all permutations of the given list of the
    pieces, then return in a list of pieces tuple.

    Keyword arguments:

    piece_dict -- The pieces dictionary with the quantity of each piece.

    """

    sequences = []
    sequence = basic_sequence(piece_dict)
    # Create permutations with itertools.permutations, then return a set of it
    for permutation in unique(itertools.permutations(sequence)):
        sequences.append(permutation)
    return sequences

def piece_sequence(sequence):
    """ Returns a list of Piece objects """
    return pieces.PieceFactory.generate_pieces(sequence)
