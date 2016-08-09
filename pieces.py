#!/usr/bin/python
#
# Unique Combinations python app
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#
# Deprecated module

"""" Zones module with adjacencies handling """

import logging

X = 0
Y = 1

class Piece(object):
    """ Base piece class """
    # 0, 1, 2, 3, 4, 5, 6, 7 are constants to North, East, South, West,
    # Northeast, Southeast, South-west and Northwest, respectively.
    NORTH, EAST, SOUTH, WEST, NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST = [x for x in range(8)]
    def __init__(self, let, mov=[0 for _ in range(8)]):
        self.movements = mov
        self.adjacencies = []
        self.letter = let

    def check_zone(self, direction, board, pos):
        """ Check adjacency zone base method """
        pass

    def prepare_adj(self, board, pos_x, pos_y, sqt=(0, 0, 0)):
        """ Prepare adjacencies base method """
        pass

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """ Check adjacencies base method """
        pass

class SquarePiece(Piece):
    """ Piece with n squares movement base class """
    def __init__(self, letter, movement=[0 for _ in range(8)]):
        Piece.__init__(letter, movement)
        self.square_adjacencies = [_ for _ in range(8)]
        self.square_relations = []

    def check_zone(self, direction, board, pos):
        """

        Verify the threat zone for horizontal and vertical 1 - n squares
        for a given piece and a given direction (N, E, S, W).

        Keyword arguments:

        direction -- Direction of the check (N, E, S, W)
        adjacencies -- List with available adjacencies
        board -- Matrix main chessboard
        pos -- Position tuple (X,Y) of the piece

        """

        adjacencies = self.square_adjacencies[direction]
        logging.debug("Checking zone on direction %s in position (%s)", direction, pos)
        for adj in adjacencies:
            adj_x, adj_y = adj
            if board[adj_x][adj_y] != 0:
                return True
            logging.debug("Checked (%d, %d) as a valid adjacency for the piece in (%s)",
                          adj_x, adj_y, pos)
        return False

    def append_adj(self, direction, position):
        """ Append adjacencies to squares and the main list """
        self.square_adjacencies[direction].append(position)
        self.adjacencies.append(position)

    def prepare_squares(self, squares):
        """ Skeleton function for prepare_squares """
        pass

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """

        Check all the adjacencies of the given piece,
        with check_zone() function.

        Keyword arguments:

        boundaries -- List with available zone to explore
        board -- Chessboard main matrix to be analyzed
        pos_x -- X Position of the piece
        pos_y -- Y Position of the piece

        """

        pos = (pos_x, pos_y)
        is_occupied = False

        # Get the board extremities and squares to be iterated
        ext = (len(board[0]), len(board))

        # Calculate the size of squares to be verified
        squares = pos[Y] - 1, pos[X] - 1, (ext[Y] - pos[Y]) - 1, (ext[X] - pos[X]) - 1
        self.prepare_squares(squares)

        # Iterate over the available directions and verify if it's
        # viable to put the piece in this position
        for drc, direction in enumerate(boundaries):
            # Verify if this piece can go this direction
            if self.movements[drc] == 0:
                return
            # Verify all the possible direction adjacencies
            self.prepare_adj(board, pos_x, pos_y, self.square_relations[direction])
            is_occupied = self.check_zone(direction, board, pos)

        return is_occupied


class King(Piece):
    """ King piece class """

    def __init__(self):
        Piece.__init__('K', [1, 1, 1, 1, 1, 1, 1, 1])

    def check_zone(self, direction, board, pos):
        """ Check king piece zone method """

        adj_x, adj_y = self.adjacencies[direction]
        if board[adj_x][adj_y] != 0:
            return True
        logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%s)",
                      adj_x, adj_y, pos)
        return False

    def prepare_adj(self, board, pos_x, pos_y, sqt=(0, 0, 0)):
        # Adjacency parameters for the king piece
        self.adjacencies.append((pos_x - 1, pos_y)) # North
        self.adjacencies.append((pos_x, pos_y + 1)) # East
        self.adjacencies.append((pos_x + 1, pos_y)) # South
        self.adjacencies.append((pos_x, pos_y - 1)) # West
        self.adjacencies.append((pos_x - 1, pos_y + 1)) # Northeast
        self.adjacencies.append((pos_x + 1, pos_y + 1)) # Southeast
        self.adjacencies.append((pos_x + 1, pos_y - 1)) # Southwest
        self.adjacencies.append((pos_x - 1, pos_y - 1)) # Northwest

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """

        Check all the adjacencies of the given piece,
        with check_zone() functions.

        Keyword arguments:

        boundaries -- List with available zone to explore
        board -- Chessboard main matrix to be analyzed
        pos_x -- X Position of the king piece
        pos_y -- Y Position of the king piece

        """

        is_occupied = False
        pos = (pos_x, pos_y)
        self.prepare_adj(board, pos_x, pos_y)

        # Iterate over the available directions and verify if it's
        # viable to put the piece in this position
        for drc, available in enumerate(boundaries):
            # Verify if this piece can go this direction
            if self.movements[drc] == 0:
                return
            logging.debug("King type movement detected, proceding to unary limits")
            # Verify all the possible direction adjacencies
            is_occupied = self.check_zone(available, board, pos)

        return is_occupied


class Queen(SquarePiece):
    """ Queen piece class """
    def __init__(self):
        SquarePiece.__init__('Q', [2, 2, 2, 2, 2, 2, 2, 2])

    def prepare_squares(self, squares):
        """ Prepare the relation of squares """
        self.square_relations.append((squares[0], 0, 0)) # North
        self.square_relations.append((squares[1], 0, 0)) # East
        self.square_relations.append((squares[2], 0, 0)) # South
        self.square_relations.append((squares[3], 0, 0)) # West
        self.square_relations.append((0, squares[0], squares[1])) # Northeast
        self.square_relations.append((0, squares[2], squares[1])) # Southeast
        self.square_relations.append((0, squares[2], squares[3])) # Southwest
        self.square_relations.append((0, squares[2], squares[3])) # Northwest

    def prepare_adj(self, board, pos_x, pos_y, sqt=(1, 0, 0)):
        # Adjacency parameters for the queen piece
        squares, squares_x, squares_y = sqt

        for sqr in range(squares):
            self.append_adj(self.NORTH, (pos_x - (1 * sqr), pos_y)) # North
            self.append_adj(self.SOUTH, (pos_x + (1 * sqr), pos_y)) # South
            self.append_adj(self.EAST, (pos_x, pos_y + (1 * sqr))) # East
            self.append_adj(self.WEST, (pos_x, pos_y - (1 * sqr))) # West
        for sqr1, sqr2 in zip(range(squares_x), range(squares_y)):
            self.append_adj(self.NORTHEAST, (pos_x - (1 * sqr1), pos_y + (1 * sqr2))) # Northeast
            self.append_adj(self.SOUTHEAST, (pos_x + (1 * sqr1), pos_y + (1 * sqr2))) # Southeast
            self.append_adj(self.SOUTHWEST, (pos_x + (1 * sqr1), pos_y - (1 * sqr2))) # Southwest
            self.append_adj(self.NORTHWEST, (pos_x - (1 * sqr1), pos_y - (1 * sqr2))) # Northwest

class Bishop(SquarePiece):
    """ Bishop piece class """

    def __init__(self):
        SquarePiece.__init__('B', [0, 0, 0, 0, 2, 2, 2, 2])

    def prepare_squares(self, squares):
        """ Prepare the relation of squares """
        self.square_relations.append((0, 0)) # North
        self.square_relations.append((0, 0)) # East
        self.square_relations.append((0, 0)) # South
        self.square_relations.append((0, 0)) # West
        self.square_relations.append((squares[0], squares[1])) # Northeast
        self.square_relations.append((squares[2], squares[1])) # Southeast
        self.square_relations.append((squares[2], squares[3])) # Southwest
        self.square_relations.append((squares[2], squares[3])) # Northwest

    def prepare_adj(self, board, pos_x, pos_y, sqt=(0, 0)):
        # Adjacency parameters for the queen piece
        squares_x, squares_y = sqt

        for sqr1, sqr2 in zip(range(squares_x), range(squares_y)):
            self.append_adj(self.NORTHEAST, (pos_x - (1 * sqr1), pos_y + (1 * sqr2))) # Northeast
            self.append_adj(self.SOUTHEAST, (pos_x + (1 * sqr1), pos_y + (1 * sqr2))) # Southeast
            self.append_adj(self.SOUTHWEST, (pos_x + (1 * sqr1), pos_y - (1 * sqr2))) # Southwest
            self.append_adj(self.NORTHWEST, (pos_x - (1 * sqr1), pos_y - (1 * sqr2))) # Northwest

class Rook(SquarePiece):
    """ Rook piece class """

    def __init__(self):
        SquarePiece.__init__('R', [2, 2, 2, 2, 0, 0, 0, 0])

    def prepare_squares(self, squares):
        """ Prepare the relation of squares """
        self.square_relations.append(squares[0]) # North
        self.square_relations.append(squares[1]) # East
        self.square_relations.append(squares[2]) # South
        self.square_relations.append(squares[3]) # West
        self.square_relations.append(0) # Northeast
        self.square_relations.append(0) # Southeast
        self.square_relations.append(0) # Southwest
        self.square_relations.append(0) # Northwest

    def prepare_adj(self, board, pos_x, pos_y, sqt=1):
        # Adjacency parameters for the rook piece
        squares = sqt

        for sqr in range(squares):
            self.append_adj(self.NORTH, (pos_x - (1 * sqr), pos_y)) # North
            self.append_adj(self.SOUTH, (pos_x + (1 * sqr), pos_y)) # South
            self.append_adj(self.EAST, (pos_x, pos_y + (1 * sqr))) # East
            self.append_adj(self.WEST, (pos_x, pos_y - (1 * sqr))) # West

class Knight(SquarePiece):
    """ Knight piece class """

    def __init__(self):
        SquarePiece.__init__('N')

    def append_adj(self, direction, position):
        """ Append adjacencies to squares and the main list """
        self.square_adjacencies[direction].append(position)
        self.adjacencies.append(position)

    def prepare_adj(self, board, pos_x, pos_y, sqt=0):
        self.append_adj(self.NORTH, (pos_x - 2, pos_y - 1)) # North
        self.append_adj(self.SOUTH, (pos_x - 2, pos_y + 1)) # South
        self.append_adj(self.EAST, (pos_x + 1, pos_y - 2)) # East
        self.append_adj(self.WEST, (pos_x - 1, pos_y - 2)) # West
        self.append_adj(self.NORTHEAST, (pos_x + 1, pos_y + 2)) # Northeast
        self.append_adj(self.SOUTHEAST, (pos_x + 2, pos_y + 1)) # Southeast
        self.append_adj(self.SOUTHWEST, (pos_x - 1, pos_y + 2)) # Southwest
        self.append_adj(self.NORTHWEST, (pos_x + 2, pos_y - 1)) # Northwest

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """

        Check all the adjacencies of the knight piece,
        with check_kzone() special function.

        Keyword arguments:

        zone -- List with available zone to explore
        board -- Chessboard main matrix to be analyzed
        pos_x -- X Position tuple of the piece
        pos_y -- Y Position tuple of the piece

        """
        pos = (pos_x, pos_y)
        ext = (len(board[0]), len(board))
        is_occupied = False
        # North direction adjacencies with special extemities
        if self.NORTH in boundaries and pos[X] >= 2:
            is_occupied = self.check_zone(self.NORTH, board, pos)
        if self.SOUTH in boundaries and pos[X] >= 2:
            is_occupied = self.check_zone(self.SOUTH, board, pos)
        if self.WEST in boundaries and pos[Y] >= 2:
            is_occupied = self.check_zone(self.WEST, board, pos)
        if self.EAST in boundaries and pos[Y] >= 2:
            is_occupied = self.check_zone(self.EAST, board, pos)

        # South directions adjacencies with special extremities
        if self.WEST in boundaries and (ext[X] - pos[Y]) >= 2:
            is_occupied = self.check_zone(self.EAST, board, pos)
        if self.EAST in boundaries and (ext[Y] - pos[Y]) >= 2:
            is_occupied = self.check_zone(self.NORTHEAST, board, pos)
        if self.SOUTH in boundaries and (ext[X] - pos[X]) >= 2:
            is_occupied = self.check_zone(self.SOUTHEAST, board, pos)
        if self.NORTH in boundaries and (ext[X] - pos[X]) >= 2:
            is_occupied = self.check_zone(self.NORTHWEST, board, pos)

        return is_occupied

class PieceFactory(object):
    """ Piece Factory pattern class """
    @staticmethod
    def generate_pieces(types):
        """ Factory method for a list of chessboard pieces """
        for typ in types:
            PieceFactory.generate_piece(typ)

    @staticmethod
    def generate_piece(typ):
        """ Factory method for chessboard pieces """
        if typ is 'K':
            return King()
        elif typ is 'Q':
            return Queen()
        elif typ is 'B':
            return Bishop()
        elif typ is 'R':
            return Rook()
        elif typ is 'N':
            return Knight()
