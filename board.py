#!/usr/bin/python
#
# Unique Combinations python app
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

""" Unique module with main functions """

import logging
import itertools
import pieces

class Board(object):
    """
    Board class
    """
    # 0 - free to use
    # 1 - threat zone
    # Unicode - piece placed
    FREE, THREAT = [x for x in range(2)]
    def __init__(self, columns, rows):
        self.board = [[0] * columns for _ in itertools.repeat(None, rows)]

    def prepare_boundaries(self, pos_x, pos_y):
        """

        Verify the boundaries of the square that the
        piece will be put.

        Keyword arguments:

        board -- The chessboard matrix with integer codes
        pos_x -- X position on the chessboard to put the piece
        pos_y -- Y position on the chessboard to put the piece

        """

        ext_x, ext_y = (len(self.board[0]) - 1, len(self.board) - 1)

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

    def insert_piece(self, piece, pos_x, pos_y):
        """

        Put the given piece in the board with its adjacencies included.

        Keyword arguments:

        piece -- Piece object that will be inserted
        board -- Main matrix chessboard to be manipulated
        x -- X position of the given piece
        y -- Y position of the given piece

        """
        logging.debug("Board before insertion of %s in (%d, %d): %s",
                      piece.letter, pos_x, pos_y, self.board)
        # Put the piece with the unicode representation on board
        self.board[pos_y][pos_x] = ord(str(piece))

        logging.debug("List of adjacencies of %s for (%d, %d): %s",
                      piece.letter, pos_x, pos_y, piece.adjacencies)
        # Insert all the adjacencies related to the piece
        for _, adj in piece.adjacencies.items():
            if isinstance(adj, list):
                for adj_t in adj:
                    adj_x, adj_y = adj_t
                    self.board[adj_y][adj_x] = self.THREAT
            else:
                adj_x, adj_y = adj
                self.board[adj_y][adj_x] = self.THREAT
        logging.debug("Board after insertion of %s in (%d, %d): %s",
                      piece.letter, pos_x, pos_y, self.board)

    def insert(self, piece):
        """

        Inserts a piece on the board. Verify adjacencies and boundaries with
        pieces classes and, if there is a valid position, the function proceed
        to piece insertion, in unicode character.

        Keyword arguments:

        piece -- Given piece instance with its properties

        """
        for pos_y, row in enumerate(self.board):
            for pos_x, square in enumerate(row):
                # Verify if the position has threat or piece placed
                logging.debug("Starting to check piece %s in position (%d,%d)",
                              piece, pos_x, pos_y)
                if square != 0:
                    continue

                boundaries = self.prepare_boundaries(pos_x, pos_y)
                # Verify if the adjacencies of the position are available
                if piece.check_adj(boundaries, self.board, pos_x, pos_y):
                    logging.info("Found threat zone, skipping this position")
                    continue
                else:
                    logging.debug("Putting piece %s on board", piece)
                    self.insert_piece(piece, pos_x, pos_y)
                    return True
        # Didn't found a suitable position for the piece on board
        return False

    def unique_configuration(self, sequence):
        """

        Search for a unique configuration for a given
        sequence of pieces on a chessboard with given
        dimensions.

        Keyword arguments:

        sequence -- A permutated sequence of pieces
        board -- The chessboard matrix with integer codes

        """

        pieces_inserted = 0
        # Verify if there is more piece to put in the board
        logging.debug("Working with sequence %s", sequence)
        chess_pieces = pieces.PieceFactory.generate_pieces(sequence)
        for piece in chess_pieces:
            logging.debug("Preparing for unique configuration for %s piece", piece)
            if self.insert(piece):
                pieces_inserted += 1
        # Verify if all the pieces were placed on chessboard
        return pieces_inserted == len(sequence)

    def __str__(self):
        """

        String representation of the board. Unicode character for the piece,
        1 for threat zone and 0 for empty zone.

        """
        mat = ''
        for row in self.board:
            for squ in row:
                if squ > 1:
                    mat += '%s ' % chr(squ)
                else:
                    mat += '%d ' % squ
            mat += '\n'
        return mat

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
    return sequences
