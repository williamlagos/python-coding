#!/usr/bin/python
#
# Unique Combinations python app
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

"""" Pieces module with adjacencies handling """

import logging


class Piece(object):
    """
    Base piece class for adjacencies handling. Inherited by all pieces in this app

    Attributes:

    movements -- List of possible movements for the piece
    boundaries -- List with possible adjacencies in the specific position
    adjacencies -- Dict with adjacencies in specific directions (N,E,S,W,NE,SE,SW,NW)
    letter -- Piece letter representation (K,Q,B,R,N)
    """
    # 0, 1, 2, 3, 4, 5, 6, 7 are constants to North, East, South, West,
    # Northeast, Southeast, South-west and Northwest, respectively.
    NORTH, EAST, SOUTH, WEST, NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST = [x for x in range(8)]
    def __init__(self, let, mov=[0 for _ in range(8)]):
        """
        Initializes Piece base class

        Keyword arguments:

        let -- The letter representing the piece (K,Q,B,R,N)
        mov -- List of size 8 with possible movements in any directions (N,E,S,W,NE,SE,SW,NW)
        """
        self.movements = mov
        self.adjacencies = {}
        self.boundaries = []
        self.letter = let

    def check_zone(self, direction, board, pos):
        """ Check adjacency zone base method """
        pass

    def prepare_adj(self, board, pos_x, pos_y):
        """ Prepare adjacencies base method """
        pass

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """ Check adjacencies base method """
        pass

    def __str__(self):
        return self.letter

class SquarePiece(Piece):
    """
    Piece with n squares movement base class. It extends the base Piece class
    adding 2 - n squares movement in the adjacencies relation

    Attributes:

    for each direction
    """
    def __init__(self, letter, movement=[0 for _ in range(8)]):
        """
        Initializes Piece base class

        Keyword Arguments:

        letter -- The letter representing the piece (K,Q,B,R,N)
        movement -- List of size 8 with possible movements in any directions (N,E,S,W,NE,SE,SW,NW)
        """

        Piece.__init__(self, letter, movement)

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

        adjacencies = self.adjacencies[direction]
        logging.debug("Checking zone %s on direction %s in (%s)", adjacencies, direction, pos)
        for adj in adjacencies:
            adj_x, adj_y = adj
            logging.debug("Checking (%d, %d) as a valid adjacency", adj_x, adj_y)
            if board[adj_x][adj_y] != 0:
                return True
            logging.debug("Checked (%d, %d) as a valid adjacency for the piece in (%s)",
                          adj_x, adj_y, pos)
        return False

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
        self.boundaries = boundaries
        self.prepare_adj(board, pos_x, pos_y)

        # Iterate over the available directions and verify if it's
        # viable to put the piece in this position
        for direction in boundaries:
            # Verify all the possible direction adjacencies
            is_occupied = self.check_zone(direction, board, pos)

        return is_occupied


class King(Piece):
    """
    King piece class, inherited from original Piece class, determines the possible
    movements and adjacencies of the King (K) chessboard piece.
    """

    def __init__(self):
        """ Initializes King piece class """

        Piece.__init__(self, 'K', [1, 1, 1, 1, 1, 1, 1, 1])

    def check_zone(self, direction, board, pos):
        """

        Checks King piece zone with the adjacencies relation.

        Keyword arguments:

        direction -- Direction code to be checked (N,E,S,W,NE,SE,SW,NW)
        board -- Chessboard matrix to be analyzed
        pos -- Position tuple (X,Y) of possible insertion

        """

        adj_x, adj_y = self.adjacencies[direction]
        logging.debug("Adjacency relation: %s", self.adjacencies)
        logging.debug("Board to be verified on adjacency (%d,%d): %s", adj_x, adj_y, board)
        if board[adj_x][adj_y] != 0:
            logging.debug("(%d, %d) is not a valid adjacency, zone checked.", adj_x, adj_y)
            return True
        logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%s)",
                      adj_x, adj_y, pos)
        return False

    def prepare_adj(self, board, pos_x, pos_y):
        """

        Add all possible adjacencies of the king piece in a given position.

        Keyword arguments:

        board -- Chessboard matrix
        pos_x -- X Position of the given piece
        pos_y -- Y Position of the given piece
        sqt -- List of squares configuration tuples. Not used here

        """
        # Adjacency parameters for the king piece
        adj = {}
        adj[self.NORTH] = (pos_x, pos_y - 1) # North
        adj[self.EAST] = (pos_x + 1, pos_y) # East
        adj[self.SOUTH] = (pos_x, pos_y + 1) # South
        adj[self.WEST] = (pos_x - 1, pos_y) # West
        adj[self.NORTHEAST] = (pos_x + 1, pos_y - 1) # Northeast
        adj[self.SOUTHEAST] = (pos_x + 1, pos_y + 1) # Southeast
        adj[self.SOUTHWEST] = (pos_x - 1, pos_y + 1) # Southwest
        adj[self.NORTHWEST] = (pos_x - 1, pos_y - 1) # Northwest
        self.adjacencies = {_ : adj[_] for _ in self.boundaries}
        logging.debug("Adjacencies relation for position (%d,%d): %s",
                      pos_x, pos_y, self.adjacencies)

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
        self.boundaries = boundaries
        self.prepare_adj(board, pos_x, pos_y)

        # Iterate over the available directions and verify if it's
        # viable to put the piece in this position
        for direction in boundaries:
            logging.info("King type movement detected, proceding to unary limits")
            logging.debug("Checking zone for direction %d", direction)
            # Verify all the possible direction adjacencies
            is_occupied = self.check_zone(direction, board, pos)

        return is_occupied


class Queen(SquarePiece):
    """
    Queen piece class, inherited from SquarePiece class, determines the possible
    movements and adjacencies of the Queen (Q) chessboard piece.
    """

    def __init__(self):
        """ Initializes Queen piece class """
        SquarePiece.__init__(self, 'Q', [2, 2, 2, 2, 2, 2, 2, 2])

    def prepare_adj(self, board, pos_x, pos_y):
        """

        Adds all possible adjacencies to the given piece

        Keyword arguments:

        board -- Matrix with possible positions
        pos_x -- X position of piece that will be placed
        pos_y -- Y position of piece that will be placed

        """

        # Adjacency parameters for the queen piece
        ext_x, ext_y = len(board[0]), len(board)
        squares_north = reversed(range(pos_y - 1)) # North
        squares_south = range(pos_y + 1, ext_y - pos_y) # South
        squares_west = reversed(range(pos_x - 1)) # West
        squares_east = range(pos_x + 1, ext_x - pos_x) # East

        north, west, east, south = [], [], [], []

        for sqr_y in squares_north:
            north.append((pos_x, sqr_y))
        for sqr_y in squares_south:
            south.append((pos_y, sqr_y))
        for sqr_x in squares_west:
            west.append((sqr_x, pos_y))
        for sqr_x in squares_east:
            east.append((sqr_x, pos_y))

        logging.debug("Horizontal and vertical squares for Queen in (%d,%d): %s; %s; %s; %s",
                      pos_x, pos_y, squares_west, squares_east, squares_north, squares_south)

        northeast, southeast, southwest, northwest = [], [], [], []

        squares_northeast = zip(range(pos_x + 1, ext_x - pos_x),
                                reversed(range(pos_y - 1,)))
        squares_southeast = zip(range(pos_x + 1, ext_x - pos_x),
                                range(pos_y + 1, ext_y - pos_y))
        squares_southwest = zip(reversed(range(pos_x - 1)),
                                range(pos_y + 1, ext_y - pos_y))
        squares_northwest = zip(reversed(range(pos_x - 1)),
                                reversed(range(pos_y - 1)))

        for sqr_x, sqr_y in squares_northeast:
            northeast.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in squares_southeast:
            southeast.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in squares_southwest:
            southwest.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in squares_northwest:
            northwest.append((sqr_x, sqr_y))

        logging.debug("Diagonal squares for Queen in (%d,%d): %s; %s; %s; %s", pos_x, pos_y,
                      squares_northwest, squares_southeast, squares_northeast, squares_southwest)

        adj = {}
        adj[self.EAST] = east # East
        adj[self.WEST] = west # West
        adj[self.NORTH] = north # North
        adj[self.SOUTH] = south # South
        adj[self.NORTHEAST] = northeast # Northeast
        adj[self.SOUTHEAST] = southeast # Southeast
        adj[self.SOUTHWEST] = southwest # Southwest
        adj[self.NORTHWEST] = northwest # Northwest

        # Filter adjacencies with available boundaries
        self.adjacencies = {_ : adj[_] for _ in self.boundaries}
        logging.debug("Adjacencies relation for position (%d,%d): %s",
                      pos_x, pos_y, self.adjacencies)

class Bishop(SquarePiece):
    """
    Bishop piece class, inherited from SquarePiece class, determines the possible
    movements and adjacencies of the Bishop (B) chessboard piece.
    """

    def __init__(self):
        """ Initializes Bishop piece class """
        SquarePiece.__init__(self, 'B', [0, 0, 0, 0, 2, 2, 2, 2])

    def prepare_adj(self, board, pos_x, pos_y):
        """

        Adds all possible adjacencies to the given piece

        Keyword arguments:

        board -- Matrix with possible positions
        pos_x -- X position of piece that will be placed
        pos_y -- Y position of piece that will be placed

        """
        ext_x, ext_y = len(board[0]), len(board)

        northeast, southeast, southwest, northwest = [], [], [], []

        squares_northeast = zip(range(pos_x + 1, ext_x - pos_x),
                                reversed(range(pos_y - 1,)))
        squares_southeast = zip(range(pos_x + 1, ext_x - pos_x),
                                range(pos_y + 1, ext_y - pos_y))
        squares_southwest = zip(reversed(range(pos_x - 1)),
                                range(pos_y + 1, ext_y - pos_y))
        squares_northwest = zip(reversed(range(pos_x - 1)),
                                reversed(range(pos_y - 1)))

        for sqr_x, sqr_y in squares_northeast:
            northeast.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in squares_southeast:
            southeast.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in squares_southwest:
            southwest.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in squares_northwest:
            northwest.append((sqr_x, sqr_y))

        logging.debug("Diagonal squares for Bishop in (%d,%d): %s; %s; %s; %s", pos_x, pos_y,
                      squares_northwest, squares_southeast, squares_northeast, squares_southwest)

        adj = {}
        adj[self.NORTHEAST] = northeast # Northeast
        adj[self.SOUTHEAST] = southeast # Southeast
        adj[self.SOUTHWEST] = southwest # Southwest
        adj[self.NORTHWEST] = northwest # Northwest

        # Filter adjacencies with available boundaries
        self.adjacencies = {_ : adj[_] for _ in self.boundaries}
        logging.debug("Adjacencies relation for position (%d,%d): %s",
                      pos_x, pos_y, self.adjacencies)

class Rook(SquarePiece):
    """
    Rook piece class, inherited from SquarePiece class, determines the possible
    movements and adjacencies of the Rook/Castle (R) chessboard piece.
    """

    def __init__(self):
        """ Initializes Rook piece class """
        SquarePiece.__init__(self, 'R', [2, 2, 2, 2, 0, 0, 0, 0])

    def prepare_adj(self, board, pos_x, pos_y):
        """

        Adds all possible adjacencies to the given piece

        Keyword arguments:

        board -- Matrix with possible positions
        pos_x -- X position of piece that will be placed
        pos_y -- Y position of piece that will be placed
        sqt -- Inherited squares configuration, used for Rook 2 - n squares movement.

        """
        # Adjacency parameters for the queen piece
        ext_x, ext_y = len(board[0]), len(board)
        squares_north = reversed(range(pos_y - 1)) # North
        squares_south = range(pos_y + 1, ext_y - pos_y) # South
        squares_west = reversed(range(pos_x - 1)) # West
        squares_east = range(pos_x + 1, ext_x - pos_x) # East

        north, west, east, south = [], [], [], []

        for sqr_y in squares_north:
            north.append((pos_x, sqr_y))
        for sqr_y in squares_south:
            south.append((pos_y, sqr_y))
        for sqr_x in squares_west:
            west.append((sqr_x, pos_y))
        for sqr_x in squares_east:
            east.append((sqr_x, pos_y))

        logging.debug("Horizontal and vertical squares for Queen in (%d,%d): %s; %s; %s; %s",
                      pos_x, pos_y, squares_west, squares_east, squares_north, squares_south)

        adj = {}
        adj[self.EAST] = east # East
        adj[self.WEST] = west # West
        adj[self.NORTH] = north # North
        adj[self.SOUTH] = south # South

        # Filter adjacencies with available boundaries
        self.adjacencies = {_ : adj[_] for _ in self.boundaries}
        logging.debug("Adjacencies relation for position (%d,%d): %s",
                      pos_x, pos_y, self.adjacencies)

class Knight(Piece):
    """

    Knight piece class, inherited from SquarePiece class, determines the possible
    movements and adjacencies of the Knight (N) chessboard piece.

    """

    NORTHERN1, NORTHERN2, NORTHERN3, NORTHERN4, SOUTHERN1, SOUTHERN2, SOUTHERN3, SOUTHERN4 = [x for x in range(8)]
    def __init__(self):
        """ Initializes Knight piece class """
        Piece.__init__(self, 'N')

    def prepare_adj(self, board, pos_x, pos_y):
        """

        Add all possible adjacencies to the piece with the given rules

        Keyword arguments:

        board -- Matrix with possible positions
        pos_x -- X position of piece that will be placed
        pos_y -- Y position of piece that will be placed

        """
        logging.debug("Preparing adjacencies of Knight in (%d,%d)", pos_x, pos_y)
        adj = {}
        adj[self.NORTHERN1] = (pos_x - 1, pos_y - 2)
        adj[self.NORTHERN2] = (pos_x + 1, pos_y - 2)
        adj[self.NORTHERN3] = (pos_x - 2, pos_y - 1)
        adj[self.NORTHERN4] = (pos_x + 2, pos_y - 1)
        adj[self.SOUTHERN1] = (pos_x - 1, pos_y + 2)
        adj[self.SOUTHERN2] = (pos_x + 1, pos_y + 2)
        adj[self.SOUTHERN3] = (pos_x + 2, pos_y + 1)
        adj[self.SOUTHERN4] = (pos_x - 2, pos_y + 1)

        # Filter adjacencies with available boundaries
        self.adjacencies = {_ : adj[_] for _ in self.boundaries}

    def check_boundaries(self, board, pos_x, pos_y):
        """Checks the special knight boundaries"""

        # if pos_x >= 1 and pos_y >= 2:

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """

        Check all the adjacencies of the knight piece,
        with check_zone() function.

        Keyword arguments:

        zone -- List with available zone to explore
        boundaries - List of possible directions due to board boundaries
        board -- Chessboard main matrix to be analyzed
        pos_x -- X Position tuple of the piece
        pos_y -- Y Position tuple of the piece

        """
        is_occupied = False
        pos = (pos_x, pos_y)
        ext_x, ext_y = len(board[0]), len(board)
        self.boundaries = boundaries
        self.prepare_adj(board, pos_x, pos_y)

        # Northern direction adjacencies with special extemities
        if self.NORTH in boundaries and pos_y >= 2:
            is_occupied = self.check_zone(self.NORTHERN1, board, pos)
        if self.SOUTH in boundaries and pos_y >= 2:
            is_occupied = self.check_zone(self.NORTHERN2, board, pos)
        if self.WEST in boundaries and pos_x >= 2:
            is_occupied = self.check_zone(self.NORTHERN3, board, pos)
        if self.EAST in boundaries and pos_x >= 2:
            is_occupied = self.check_zone(self.NORTHERN4, board, pos)

        # Southern directions adjacencies with special extremities
        if self.WEST in boundaries and (ext_y - pos_y) >= 2:
            is_occupied = self.check_zone(self.SOUTHERN1, board, pos)
        if self.EAST in boundaries and (ext_x - pos_x) >= 2:
            is_occupied = self.check_zone(self.SOUTHERN2, board, pos)
        if self.SOUTH in boundaries and (ext_y - pos_y) >= 2:
            is_occupied = self.check_zone(self.SOUTHERN3, board, pos)
        if self.NORTH in boundaries and (ext_x - pos_x) >= 2:
            is_occupied = self.check_zone(self.SOUTHERN4, board, pos)

        return is_occupied

class PieceFactory(object):
    """

    Piece Factory pattern class. It generates automatically all the pieces
    with the Factory pattern

    """
    @staticmethod
    def generate_pieces(types):
        """

        Factory method for a list of chessboard pieces

        Keyword arguments:

        types -- List of pieces with the given types

        """
        pieces = []
        for typ in types:
            pieces.append(PieceFactory.generate_piece(typ))
        return pieces

    @staticmethod
    def generate_piece(typ):
        """

        Factory method for chessboard pieces

        Keyword arguments:

        typ -- Piece with a given type

        """
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
