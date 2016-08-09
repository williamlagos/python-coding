#!/usr/bin/python
#
# Unique Combinations python app
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#
# Deprecated module

"""" Zones module with adjacencies handling """

import logging

class Piece:
    """ Base piece class """
    # 0, 1, 2, 3, 4, 5, 6, 7 are constants to North, East, South, West,
    # Northeast, Southeast, South-west and Northwest, respectively.
    NORTH, EAST, SOUTH, WEST, NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST = [x for x in range(8)]
    def __init__(self, mov=[0 for x in range(8)]):
        self.movements = mov

class King(Piece):
    """ King piece class """
    def __init__(self):
        Piece.__init__([1, 1, 1, 1, 1, 1, 1, 1])

class Queen(Piece):
    """ Queen piece class """
    def __init__(self):
        Piece.__init__([2, 2, 2, 2, 2, 2, 2, 2])

class Bishop(Piece):
    """ Bishop piece class """

    def __init__(self):
        Piece.__init__([0, 0, 0, 0, 2, 2, 2, 2])

    def check_dzone(self, direction, adjacencies, squares, board, pos):
        """

        Verify the threat zone for diagonal 1 - n squares
        for a given piece and a given direction (N, E, S, W).

        Keyword arguments:

        direction -- Direction of the check (N, E, S, W)
        adjacencies -- List with available adjacencies
        squares -- Tuple of squares to be verified on (X,Y) coordinate
        board -- Matrix main chessboard
        pos -- Position tuple (X,Y) of the piece

        """

        adj_x = adj_y = 0
        logging.debug("Checking diagonal zone on direction %s in position (%s)",
                      direction, pos)
        logging.debug("Number of squares to be checked: X:%d Y:%d", squares[0], squares[1])
        # if squares is 1, it'll iterate just one time (K movement)
        for sqr1, sqr2 in zip(range(squares[0]), range(squares[1])):
            # Northeast direction
            if direction is NE:
                adj_x = pos[X] - (1 * sqr1)
                adj_y = pos[Y] + (1 * sqr2)
            # Southeast direction
            elif direction is SE:
                adj_x = pos[X] + (1 * sqr1)
                adj_y = pos[Y] + (1 * sqr2)
            # South-west direction
            elif direction is SW:
                adj_x = pos[X] + (1 * sqr1)
                adj_y = pos[Y] - (1 * sqr2)
            # Northwest direction
            elif direction is NW:
                adj_x = pos[X] - (1 * sqr1)
                adj_y = pos[Y] - (1 * sqr2)
            if board[adj_x][adj_y] != FREE:
                return True
            else:
                adjacencies.append((adj_x, adj_y))
                logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%s)",
                              adj_x, adj_y, pos)
        return False

class Rook(Piece):
    """ Rook piece class """

    def __init__(self):
        Piece.__init__([2, 2, 2, 2, 0, 0, 0, 0])

    def check_zone(self, direction, adjacencies, squares, board, pos):
        """

        Verify the threat zone for horizontal and vertical 1 - n squares
        for a given piece and a given direction (N, E, S, W).

        Keyword arguments:

        direction -- Direction of the check (N, E, S, W)
        adjacencies -- List with available adjacencies
        squares -- Number of squares to be verified
        board -- Matrix main chessboard
        pos -- Position tuple (X,Y) of the piece

        """

        adj_x = adj_y = 0
        logging.debug("Checking zone on direction %s in position (%s)", direction, pos)
        logging.debug("Number of squares to be checked: %d", squares)
        # if squares is 1, it'll iterate just one time (K movement)
        for sqr in range(squares):
            # North direction
            if direction is N:
                adj_x = pos[X] - (1 * sqr)
                adj_y = pos[Y]
            # East direction
            elif direction is E:
                adj_x = pos[X]
                adj_y = pos[Y] + (1 * sqr)
            # South direction
            elif direction is S:
                logging.info("Got south direction")
                adj_x = pos[X] + (1 * sqr)
                adj_y = pos[Y]
                logging.debug("(%d,%d)", adj_x, adj_y)
            # West direction
            elif direction is W:
                adj_x = pos[X]
                adj_y = pos[Y] - (1 * sqr)
            if board[adj_x][adj_y] != FREE:
                return True
            else:
                adjacencies.append((adj_x, adj_y))
                logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%s)",
                              adj_x, adj_y, pos)
        return False


class Knight(Piece):
    """ Knight piece class """

    def __init__(self):
        Piece.__init__()

    def check_nzone(self, direction, adjacencies, board, pos_x, pos_y):
        """

        Verify the threat zone for knight special squares
        for a given piece and a given direction (N, E, S, W, NE, SE, SW, NW).

        Keyword arguments:

        direction -- Direction of the check (N, E, S, W, NE, SE, SW, NW)
        adjacencies -- List with available adjacencies
        board -- Matrix main chessboard
        pos_x -- X position of the piece
        pos_y -- Y position of the piece

        """

        adj_x = adj_y = 0
        logging.debug("Checking knight zone on direction %s in position (%d, %d)",
                      direction, pos_x, pos_y)
        # North knight direction
        if direction is N:
            adj_x = pos_x - 2
            adj_y = pos_y - 1
        # East knight direction
        elif direction is E:
            adj_x = pos_x + 1
            adj_y = pos_y - 2
        # South knight direction
        elif direction is S:
            adj_x = pos_x - 2
            adj_y = pos_y + 1
        # West knight direction
        elif direction is W:
            adj_x = pos_x - 1
            adj_y = pos_y - 2
        # Northeast knight direction
        elif direction is NE:
            adj_x = pos_x + 1
            adj_y = pos_y + 2
        # Southeast knight direction
        elif direction is SE:
            adj_x = pos_x + 2
            adj_y = pos_y + 1
        # Southwest knight direction
        elif direction is SW:
            adj_x = pos_x - 1
            adj_y = pos_y + 2
        # Northwest knight direction
        elif direction is NW:
            adj_x = pos_x + 2
            adj_y = pos_y - 1
        if board[adj_x][adj_y] != FREE:
            return True
        else:
            adjacencies.append((adj_x, adj_y))
            logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%d, %d)",
                          adj_x, adj_y, pos_x, pos_y)
            return False

    def check_knight_adjacencies(self, zone, adj, board, pos):
        """

        Check all the adjacencies of the knight piece,
        with check_kzone() special function.

        Keyword arguments:

        zone -- List with available zone to explore
        adj -- Adjacencies tuple (X,Y) list to be handled
        board -- Chessboard main matrix to be analyzed
        pos -- Position tuple (X,Y) of the given piece

        """
        ext = (len(board[0]), len(board))
        is_adjacency_occupied = False
        # North direction adjacencies with special extemities
        if N in zone and pos[X] >= 2 and self.check_nzone(N, adj, board, pos[X], pos[Y]):
            is_adjacency_occupied = True
        if S in zone and pos[X] >= 2 and self.check_nzone(S, adj, board, pos[X], pos[Y]):
            is_adjacency_occupied = True
        if W in zone and pos[Y] >= 2 and self.check_nzone(W, adj, board, pos[X], pos[Y]):
            is_adjacency_occupied = True
        if E in zone and pos[Y] >= 2 and self.check_nzone(E, adj, board, pos[X], pos[Y]):
            is_adjacency_occupied = True

        # South directions adjacencies with special extremities
        if W in zone and (ext[X] - pos[Y]) >= 2 and self.check_nzone(SW, adj, board, pos[X], pos[Y]):
            is_adjacency_occupied = True
        if E in zone and (ext[Y] - pos[Y]) >= 2 and self.check_nzone(NE, adj, board, pos[X], pos[Y]):
            is_adjacency_occupied = True
        if S in zone and (ext[X] - pos[X]) >= 2 and self.check_nzone(SE, adj, board, pos[X], pos[Y]):
            is_adjacency_occupied = True
        if N in zone and (ext[X] - pos[X]) >= 2 and self.check_nzone(NW, adj, board, pos[X], pos[Y]):
            is_adjacency_occupied = True

        return is_adjacency_occupied


# deprecated constants
N = 0
E = 1
S = 2
W = 3
NE = 4
SE = 5
SW = 6
NW = 7
FREE = 0
THREAT = 1
X = 0
Y = 1

class PieceFactory:
    """ Piece Factory pattern class """
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

def check_adjacencies(zone, directions, adj, board, pos):
    """

    Check all the adjacencies of the given piece,
    with check_zone() and check_dzone() functions.

    Keyword arguments:

    zone -- List with available zone to explore
    directions -- Movement types list of the given piece
    adj -- Adjacencies tuple (X,Y) list to be handled
    board -- Chessboard main matrix to be analyzed
    pos -- Position tuple (X,Y) of the given piece

    """
    # ext = (len(board[0]), len(board))
    is_adjacency_occupied = False
    # Iterate over the available directions and verify if it's
    # viable to put the piece in this position
    # sqr = (1, 1, 1, 1)
    for drc, available in enumerate(zone):
        # Verify if this piece can go this direction
        if directions[drc] == 0:
            return
        # Verify if the directions of this piece are just one
        # square per time or the entire row/column
        # if directions[drc] > 1:
        #     logging.debug("Movement with %d squares, proceding to board limits", directions[drc])
        #     sqr = pos[Y] - 1, pos[X] - 1, (ext[Y] - pos[Y]) - 1, (ext[X] - pos[X]) - 1
        # else:
        #     logging.debug("King type movement detected, proceding to unary limits")
        # # Verify all the possible direction adjacencies
        # if available is N and check_zone(N, adj, sqr[0], board, pos):
        #     is_adjacency_occupied = True
        # elif available is E and check_zone(E, adj, sqr[1], board, pos):
        #     is_adjacency_occupied = True
        # elif available is S and check_zone(S, adj, sqr[2], board, pos):
        #     is_adjacency_occupied = True
        # elif available is W and check_zone(W, adj, sqr[3], board, pos):
        #     is_adjacency_occupied = True
        # elif available is NE and check_dzone(NE, adj, (sqr[0], sqr[1]), board, pos):
        #     is_adjacency_occupied = True
        # elif available is SE and check_dzone(SE, adj, (sqr[2], sqr[1]), board, pos):
        #     is_adjacency_occupied = True
        # elif available is SW and check_dzone(SW, adj, (sqr[2], sqr[3]), board, pos):
        #     is_adjacency_occupied = True
        # elif available is NW and check_dzone(NW, adj, (sqr[2], sqr[3]), board, pos):
        #     is_adjacency_occupied = True
    return is_adjacency_occupied
