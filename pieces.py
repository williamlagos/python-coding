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

class Piece:
    """ Base piece class """
    # 0, 1, 2, 3, 4, 5, 6, 7 are constants to North, East, South, West,
    # Northeast, Southeast, South-west and Northwest, respectively.
    NORTH, EAST, SOUTH, WEST, NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST = [x for x in range(8)]
    def __init__(self, let, mov=[0 for x in range(8)]):
        self.movements = mov
        self.adjacencies = []
        self.letter = let

    def prepare_adj(self, board, pos_x, pos_y, sqt=(1, 1, 1)):
        """ Prepare adjacencies base method """
        pass

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """ Check adjacencies base method """
        pass

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

    def prepare_adj(self, board, pos_x, pos_y, sqt=(1, 1, 1)):
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


class Queen(Piece):
    """ Queen piece class """
    def __init__(self):
        Piece.__init__('Q', [2, 2, 2, 2, 2, 2, 2, 2])

    def check_zone(self, direction, squares, board, pos):
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

        local_adjacencies = []
        adj = self.adjacencies[direction]
        logging.debug("Checking zone on direction %s in position (%s)", direction, pos)
        logging.debug("Number of squares to be checked: %d", squares)
        for sqr in range(squares):
            adj_x, adj_y = adj[sqr]
            if board[adj_x][adj_y] != 0:
                return True
            local_adjacencies.append((adj_x, adj_y))
            logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%s)", adj_x, adj_y, pos)
        self.adjacencies = local_adjacencies
        return False


    def prepare_adj(self, board, pos_x, pos_y, sqt=(1, 1, 1)):
        # Adjacency parameters for the king piece
        squares, squares_x, squares_y = sqt
        for _ in range(8): self.adjacencies.append([])
        for sqr in range(squares):
            self.adjacencies[self.NORTH].append((pos_x - (1 * sqr), pos_y)) # North
            self.adjacencies[self.SOUTH].append((pos_x + (1 * sqr), pos_y)) # South
            self.adjacencies[self.EAST].append((pos_x, pos_y + (1 * sqr))) # East
            self.adjacencies[self.WEST].append((pos_x, pos_y - (1 * sqr))) # West
        for sqr1, sqr2 in zip(range(squares_x), range(squares_y)):
            self.adjacencies[self.NORTHEAST].append((pos_x - (1 * sqr1), pos_y + (1 * sqr2))) # Northeast
            self.adjacencies[self.SOUTHEAST].append((pos_x + (1 * sqr1), pos_y + (1 * sqr2))) # Southeast
            self.adjacencies[self.SOUTHWEST].append((pos_x + (1 * sqr1), pos_y - (1 * sqr2))) # Southwest
            self.adjacencies[self.NORTHWEST].append((pos_x - (1 * sqr1), pos_y - (1 * sqr2))) # Northwest

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """

        Check all the adjacencies of the given piece,
        with check_zone() function.

        Keyword arguments:

        zone -- List with available zone to explore
        directions -- Movement types list of the given piece
        adj -- Adjacencies tuple (X,Y) list to be handled
        board -- Chessboard main matrix to be analyzed
        pos -- Position tuple (X,Y) of the given piece

        """

        pos = (pos_x, pos_y)
        is_occupied = False
        ext = (len(board[0]), len(board))
        sqr = pos[Y] - 1, pos[X] - 1, (ext[Y] - pos[Y]) - 1, (ext[X] - pos[X]) - 1

        # Iterate over the available directions and verify if it's
        # viable to put the piece in this position
        for drc, available in enumerate(boundaries):
            # Verify if this piece can go this direction
            if self.movements[drc] == 0:
                return
            # Calculate the size of squares to be verified
            logging.debug("Movement with %d squares, proceding to limits", self.movements[drc])

            # Verify all the possible direction adjacencies
            # if available is self.NORTH and
            #     self.check_zone(self.NORTH, adj, sqr[0], board, pos)):
            #     is_adjacency_occupied = True
            # elif (available is self.EAST and
            #       self.check_zone(self.EAST, adj, sqr[1], board, pos)):
            #     is_adjacency_occupied = True
            # elif (available is self.SOUTH and
            #       self.check_zone(self.SOUTH, adj, sqr[2], board, pos)):
            #     is_adjacency_occupied = True
            # elif (available is self.WEST and
            #       self.check_zone(self.WEST, adj, sqr[3], board, pos)):
            #     is_adjacency_occupied = True
            # elif (available is self.NORTHEAST and
            #       self.check_dzone(self.NORTHEAST, adj, (sqr[0], sqr[1]), board, pos)):
            #     is_adjacency_occupied = True
            # elif (available is self.SOUTHEAST and
            #       self.check_dzone(self.SOUTHEAST, adj, (sqr[2], sqr[1]), board, pos)):
            #     is_adjacency_occupied = True
            # elif (available is self.SOUTHWEST and
            #       self.check_dzone(self.SOUTHWEST, adj, (sqr[2], sqr[3]), board, pos)):
            #     is_adjacency_occupied = True
            # elif (available is self.NORTHWEST and
            #       self.check_dzone(self.NORTHWEST, adj, (sqr[2], sqr[3]), board, pos)):
            #     is_adjacency_occupied = True
        return is_adjacency_occupied

class Bishop(Piece):
    """ Bishop piece class """

    def __init__(self):
        Piece.__init__('B', [0, 0, 0, 0, 2, 2, 2, 2])

    def check_dzone(self, direction, squares, board, pos):
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
        adjacencies = self.adjacencies
        logging.debug("Checking diagonal zone on direction %s in position (%s)",
                      direction, pos)
        logging.debug("Number of squares to be checked: X:%d Y:%d", squares[0], squares[1])
        for sqr1, sqr2 in zip(range(squares[0]), range(squares[1])):
            # Northeast direction
            if direction is self.NORTHEAST:
                adj_x = pos[X] - (1 * sqr1)
                adj_y = pos[Y] + (1 * sqr2)
            # Southeast direction
            elif direction is self.SOUTHEAST:
                adj_x = pos[X] + (1 * sqr1)
                adj_y = pos[Y] + (1 * sqr2)
            # Southwest direction
            elif direction is self.SOUTHWEST:
                adj_x = pos[X] + (1 * sqr1)
                adj_y = pos[Y] - (1 * sqr2)
            # Northwest direction
            elif direction is self.NORTHWEST:
                adj_x = pos[X] - (1 * sqr1)
                adj_y = pos[Y] - (1 * sqr2)
            if board[adj_x][adj_y] != 0:
                return True
            else:
                adjacencies.append((adj_x, adj_y))
                logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%s)",
                              adj_x, adj_y, pos)
        return False

    def check_adj(self, boundaries, board, pos_x, pos_y):
        pass

class Rook(Piece):
    """ Rook piece class """

    def __init__(self):
        Piece.__init__('R', [2, 2, 2, 2, 0, 0, 0, 0])

    def check_zone(self, direction, squares, board, pos):
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
        adjacencies = self.adjacencies
        logging.debug("Checking zone on direction %s in position (%s)", direction, pos)
        logging.debug("Number of squares to be checked: %d", squares)
        # if squares is 1, it'll iterate just one time (K movement)
        for sqr in range(squares):
            # North direction
            if direction is self.NORTH:
                adj_x = pos[X] - (1 * sqr)
                adj_y = pos[Y]
            # East direction
            elif direction is self.EAST:
                adj_x = pos[X]
                adj_y = pos[Y] + (1 * sqr)
            # South direction
            elif direction is self.SOUTH:
                logging.info("Got south direction")
                adj_x = pos[X] + (1 * sqr)
                adj_y = pos[Y]
                logging.debug("(%d,%d)", adj_x, adj_y)
            # West direction
            elif direction is self.WEST:
                adj_x = pos[X]
                adj_y = pos[Y] - (1 * sqr)
            if board[adj_x][adj_y] != 0:
                return True
            else:
                adjacencies.append((adj_x, adj_y))
                logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%s)",
                              adj_x, adj_y, pos)
        return False

    def check_adj(self, boundaries, board, pos_x, pos_y):
        pass

class Knight(Piece):
    """ Knight piece class """

    def __init__(self):
        Piece.__init__('N')

    def check_nzone(self, direction, board, pos_x, pos_y):
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
        adjacencies = self.adjacencies
        logging.debug("Checking knight zone on direction %s in position (%d, %d)",
                      direction, pos_x, pos_y)
        # North knight direction
        if direction is self.NORTH:
            adj_x = pos_x - 2
            adj_y = pos_y - 1
        # East knight direction
        elif direction is self.EAST:
            adj_x = pos_x + 1
            adj_y = pos_y - 2
        # South knight direction
        elif direction is self.SOUTH:
            adj_x = pos_x - 2
            adj_y = pos_y + 1
        # West knight direction
        elif direction is self.WEST:
            adj_x = pos_x - 1
            adj_y = pos_y - 2
        # Northeast knight direction
        elif direction is self.NORTHEAST:
            adj_x = pos_x + 1
            adj_y = pos_y + 2
        # Southeast knight direction
        elif direction is self.SOUTHEAST:
            adj_x = pos_x + 2
            adj_y = pos_y + 1
        # Southwest knight direction
        elif direction is self.SOUTHWEST:
            adj_x = pos_x - 1
            adj_y = pos_y + 2
        # Northwest knight direction
        elif direction is self.NORTHWEST:
            adj_x = pos_x + 2
            adj_y = pos_y - 1
        if board[adj_x][adj_y] != 0:
            return True
        else:
            adjacencies.append((adj_x, adj_y))
            logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%d, %d)",
                          adj_x, adj_y, pos_x, pos_y)
            return False

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """

        Check all the adjacencies of the knight piece,
        with check_kzone() special function.

        Keyword arguments:

        zone -- List with available zone to explore
        adj -- Adjacencies tuple (X,Y) list to be handled
        board -- Chessboard main matrix to be analyzed
        pos -- Position tuple (X,Y) of the given piece

        """
        pos = (pos_x, pos_y)
        ext = (len(board[0]), len(board))
        is_adjacency_occupied = False
        # North direction adjacencies with special extemities
        if (self.NORTH in boundaries and pos[X] >= 2 and
                self.check_nzone(self.NORTH, board, pos[X], pos[Y])):
            is_adjacency_occupied = True
        if (self.SOUTH in boundaries and pos[X] >= 2 and
                self.check_nzone(self.SOUTH, board, pos[X], pos[Y])):
            is_adjacency_occupied = True
        if (self.WEST in boundaries and pos[Y] >= 2 and
                self.check_nzone(self.WEST, board, pos[X], pos[Y])):
            is_adjacency_occupied = True
        if (self.EAST in boundaries and pos[Y] >= 2 and
                self.check_nzone(self.EAST, board, pos[X], pos[Y])):
            is_adjacency_occupied = True

        # South directions adjacencies with special extremities
        if (self.WEST in boundaries and (ext[X] - pos[Y]) >= 2 and
                self.check_nzone(self.SOUTHWEST, board, pos[X], pos[Y])):
            is_adjacency_occupied = True
        if (self.EAST in boundaries and (ext[Y] - pos[Y]) >= 2 and
                self.check_nzone(self.NORTHEAST, board, pos[X], pos[Y])):
            is_adjacency_occupied = True
        if (self.SOUTH in boundaries and (ext[X] - pos[X]) >= 2 and
                self.check_nzone(self.SOUTHEAST, board, pos[X], pos[Y])):
            is_adjacency_occupied = True
        if (self.NORTH in boundaries and (ext[X] - pos[X]) >= 2 and
                self.check_nzone(self.NORTHWEST, board, pos[X], pos[Y])):
            is_adjacency_occupied = True

        return is_adjacency_occupied

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
