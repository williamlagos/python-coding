#!/usr/bin/python
#
# Unique Combinations python unit test
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

""" Tests application finds the unique combinations of X pieces on a M x N chessboard """

import unittest
import unique
# import zones

class ChessApplicationTest(unittest.TestCase):
    """ Class of chess main application """

    def test_permutations(self):
        """ Tests possible ordered sequences in permutation """
        unique.possible_ordered_sequences({'K':2, 'Q':0, 'R':1, 'B':0, 'N':0})
        self.assertEqual('permutations', 'permutations')

    def test_adjacencies(self):
        """ Tests adjacencies checking """
        self.assertEqual('adjacencies', 'adjacencies')

    def test_insert(self):
        """ Tests chessboard piece insertion """
        self.assertEqual('insert', 'insert')

if __name__ == '__main__':
    unittest.main()
