#!/usr/bin/python
#
# Unique Combinations python unit test
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

""" Tests application finds the unique combinations of X pieces on a M x N chessboard """

import unittest
import itertools
import board
import pieces

class BoardApplicationTest(unittest.TestCase):
    """ Class of chess main application - board module testing """

    def test_permutations(self):
        """ Tests possible ordered sequences in permutation """
        permutations = set([('K', 'K', 'R'), ('K', 'R', 'K'), ('R', 'K', 'K')])
        result = board.possible_ordered_sequences({'K':2, 'Q':0, 'R':1, 'B':0, 'N':0})
        self.assertEqual(permutations, result)

    def test_boundaries(self):
        """ Tests boundaries checking """
        matrix = [[0] * 3 for _ in itertools.repeat(None, 3)]

        # Corner upper left boundaries
        corner_uleft_boundaries = [1, 2, 5]
        result = board.prepare_boundaries(matrix, 0, 0)
        self.assertEqual(corner_uleft_boundaries, result)

        # Corner down left boundaries
        corner_dleft_boundaries = [0, 1, 4]
        result = board.prepare_boundaries(matrix, 0, 2)
        self.assertEqual(corner_dleft_boundaries, result)

        # Between left corners boundaries
        corner_bleft_boundaries = [0, 1, 2, 4, 5]
        result = board.prepare_boundaries(matrix, 0, 1)
        self.assertEqual(corner_bleft_boundaries, result)

        # Corner upper right boundaries
        corner_uright_boundaries = [2, 3, 6]
        result = board.prepare_boundaries(matrix, 2, 0)
        self.assertEqual(corner_uright_boundaries, result)

        # Corner down right boundaries
        corner_dright_boundaries = [0, 3, 7]
        result = board.prepare_boundaries(matrix, 2, 2)
        self.assertEqual(corner_dright_boundaries, result)

        # Between corners right boundaries
        corner_bright_boundaries = [0, 2, 3, 6, 7]
        result = board.prepare_boundaries(matrix, 2, 1)
        self.assertEqual(corner_bright_boundaries, result)

        # Upper between corners boundaries
        upper_boundaries = [1, 2, 3, 5, 6]
        result = board.prepare_boundaries(matrix, 1, 0)
        self.assertEqual(upper_boundaries, result)

        # Down between corners
        down_boundaries = [0, 1, 3, 4, 7]
        result = board.prepare_boundaries(matrix, 1, 2)
        self.assertEqual(down_boundaries, result)

        # All boundaries
        boundaries = [0, 1, 2, 3, 4, 5, 6, 7]
        result = board.prepare_boundaries(matrix, 1, 1)
        self.assertEqual(boundaries, result)

    def test_insert(self):
        """ Tests chessboard piece insertion """
        result = [[0] * 3 for _ in itertools.repeat(None, 3)]
        matrix = [[75, 1, 0], [1, 1, 0], [0, 0, 0]]
        piece = pieces.PieceFactory.generate_piece('K')
        boundaries = board.prepare_boundaries(result, 0, 0)
        piece.check_adj(boundaries, result, 0, 0)
        board.insert_piece(piece, result, 0, 0)
        self.assertEqual(matrix, result)

class PiecesApplicationTest(unittest.TestCase):
    """ Class of chess main application - pieces module testing """

    def test_list_adjacencies(self):
        """ Tests adjacencies listing """
        adjacencies_list = []
        expectedadj_list = []
        piece_letters = ['K', 'Q', 'B', 'R', 'N']
        matrix = [[0] * 3 for _ in itertools.repeat(None, 3)]
        chessmans = pieces.PieceFactory.generate_pieces(piece_letters)
        boundaries = board.prepare_boundaries(matrix, 0, 0)
        # for man in chessmans:
        #     man.check_adj(boundaries, matrix, 0, 0)
        #     adjacencies_list.append(man.adjacencies)
        self.assertEqual(expectedadj_list, adjacencies_list)

    def test_adjacencies(self):
        """ Tests adjacencies checking """
        queen = pieces.PieceFactory.generate_piece('Q')
        matrix = [[0] * 3 for _ in itertools.repeat(None, 3)]
        adjacencies = {1: [(1, 0), (2, 0)], 2: [(0, 1), (0, 2)], 5: [(1, 1), (2, 2)]}
        boundaries = board.prepare_boundaries(matrix, 0, 0)
        queen.boundaries = boundaries
        queen.prepare_adj(matrix, 0, 0, (3, 3, 3))
        result = queen.adjacencies
        self.assertEqual(adjacencies, result)

if __name__ == '__main__':
    unittest.main()
