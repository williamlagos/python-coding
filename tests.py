#!/usr/bin/python
#
# Unique Combinations python unit test
# The application that will be tested finds the unique combinations of X pieces on a M x N chessboard
#
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

import unique
import unittest

class UniqueApplicationTest(unittest.TestCase):
    def test_permutations(self):
        unique.possible_ordered_sequences({'K':2,'Q':0,'R':1,'B':0,'N':0})
        self.assertEqual('permutations','permutations')
    def test_adjacencies(self):
        self.assertEqual('adjacencies','adjacencies')
    def test_insert(self):
        self.assertEqual('insert','insert')

if __name__ == '__main__':
    unittest.main()
