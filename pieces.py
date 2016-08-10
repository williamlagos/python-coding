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
        """

        Checks piece zone with the adjacencies relation.

        Keyword arguments:

        direction -- Direction code to be checked (N,E,S,W,NE,SE,SW,NW)
        board -- Chessboard matrix to be analyzed
        pos -- Position tuple (X,Y) of possible insertion

        """

        adj_x, adj_y = self.adjacencies[direction]
        logging.debug("Adjacency relation (%d,%d): %s", adj_x, adj_y, self.adjacencies)
        # Check if there is another piece in the adjacency zone. If it's just threat zone, ignore
        if board[adj_y][adj_x] > 1:
            logging.debug("(%d, %d) is not a valid adjacency, zone checked.", adj_x, adj_y)
            return True
        logging.debug("Added (%d, %d) as a valid adjacency for the piece in (%s)",
                      adj_x, adj_y, pos)
        return False

    def prepare_adj(self, board, pos_x, pos_y):
        """ Prepare adjacencies skeleton base method """
        pass

    def check_adj(self, boundaries, board, pos_x, pos_y):
        """ Check adjacencies skeleton base method """
        pass

    def __str__(self):
        """ Chess piece string representation """
        return self.letter

class SquarePiece(Piece):
    """

    Piece with n squares movement base class. It extends the base Piece class
    adding 2 - n squares movement in the adjacencies relation

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
            # Check if there is another piece in the adjacency
            # zone. If it's just threat zone, ignore
            if board[adj_y][adj_x] > 1:
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
        # Set for only valid movement boundaries for the given piece
        self.boundaries = [_ for _ in boundaries if self.movements[_] > 0]
        self.prepare_adj(board, pos_x, pos_y)

        # Iterate over the available directions and verify if it's
        # viable to put the piece in this position
        for direction in self.boundaries:
            # Verify all the possible direction adjacencies
            if self.check_zone(direction, board, pos):
                return True

        return False


class King(Piece):
    """

    King piece class, inherited from original Piece class, determines the possible
    movements and adjacencies of the King (K) chessboard piece.

    """

    def __init__(self):
        """ Initializes King piece class """

        Piece.__init__(self, 'K', [1, 1, 1, 1, 1, 1, 1, 1])

    def prepare_adj(self, board, pos_x, pos_y):
        """

        Add all possible adjacencies of the king piece in a given position.

        Keyword arguments:

        board -- Chessboard matrix
        pos_x -- X Position of the given piece
        pos_y -- Y Position of the given piece

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

        pos = (pos_x, pos_y)
        self.boundaries = boundaries
        self.prepare_adj(board, pos_x, pos_y)

        # Iterate over the available directions and verify if it's
        # viable to put the piece in this position
        for direction in boundaries:
            logging.info("King type movement detected, proceding to unary limits")
            logging.debug("Checking zone for direction %d", direction)
            # Verify all the possible direction adjacencies
            if self.check_zone(direction, board, pos):
                return True

        return False


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

        north, west, east, south = [], [], [], []

        for sqr_y in reversed(range(pos_y)): # North
            north.append((pos_x, sqr_y))
        for sqr_y in range(pos_y + 1, ext_y): # South
            south.append((pos_x, sqr_y))
        for sqr_x in reversed(range(pos_x)): # West
            west.append((sqr_x, pos_y))
        for sqr_x in range(pos_x + 1, ext_x): # East
            east.append((sqr_x, pos_y))

        logging.debug("Horizontal and vertical squares for Queen in (%d,%d): %s; %s; %s; %s",
                      pos_x, pos_y, west, east, north, south)

        northeast, southeast, southwest, northwest = [], [], [], []

        for sqr_x, sqr_y in zip(range(pos_x + 1, ext_x), # Northeast
                                reversed(range(pos_y))):
            northeast.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in zip(range(pos_x + 1, ext_x), # Southeast
                                range(pos_y + 1, ext_y)):
            southeast.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in zip(reversed(range(pos_x)),      # Southwest
                                range(pos_y + 1, ext_y)):
            southwest.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in zip(reversed(range(pos_x)),      # Northwest
                                reversed(range(pos_y))):
            northwest.append((sqr_x, sqr_y))

        logging.debug("Diagonal squares for Queen in (%d,%d): %s; %s; %s; %s", pos_x, pos_y,
                      northwest, southeast, northeast, southwest)

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

        for sqr_x, sqr_y in zip(range(pos_x + 1, ext_x), # Northeast
                                reversed(range(pos_y))):
            northeast.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in zip(range(pos_x + 1, ext_x), # Southeast
                                range(pos_y + 1, ext_y)):
            southeast.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in zip(reversed(range(pos_x)),      # Southwest
                                range(pos_y + 1, ext_y)):
            southwest.append((sqr_x, sqr_y))
        for sqr_x, sqr_y in zip(reversed(range(pos_x)),      # Northwest
                                reversed(range(pos_y))):
            northwest.append((sqr_x, sqr_y))

        logging.debug("Diagonal squares for Bishop in (%d,%d): %s; %s; %s; %s", pos_x, pos_y,
                      northwest, southeast, northeast, southwest)

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

        """

        # Adjacency parameters for the queen piece
        ext_x, ext_y = len(board[0]), len(board)

        north, west, east, south = [], [], [], []

        for sqr_y in reversed(range(pos_y)): # North
            north.append((pos_x, sqr_y))
        for sqr_y in range(pos_y + 1, ext_y): # South
            south.append((pos_x, sqr_y))
        for sqr_x in reversed(range(pos_x)): # West
            west.append((sqr_x, pos_y))
        for sqr_x in range(pos_x + 1, ext_x): # East
            east.append((sqr_x, pos_y))

        logging.debug("Horizontal and vertical squares for Rook in (%d,%d): %s; %s; %s; %s",
                      pos_x, pos_y, west, east, north, south)

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

    NORTHERN1, NORTHERN2, NORTHERN3, NORTHERN4, \
    SOUTHERN1, SOUTHERN2, SOUTHERN3, SOUTHERN4 = [x for x in range(8)]
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

    def prepare_boundaries(self, board, pos_x, pos_y):
        """

        Prepares the special knight boundaries, separating from the general
        boundaries chess logic of the program.

        Keyword arguments:

        board -- Chessboard matrix with positions
        pos_x -- X Position of the knight piece
        pos_x -- Y Position of the knight piece

        """

        boundaries = []
        ext_x, ext_y = (len(board[0]) - 1), (len(board) - 1)

        # Northern directions
        if pos_x >= 1 and pos_y >= 2:
            boundaries.append(self.NORTHERN1)
        if (ext_x - pos_x) >= 1 and pos_y >= 2:
            boundaries.append(self.NORTHERN2)
        if pos_x >= 2 and pos_y >= 1:
            boundaries.append(self.NORTHERN3)
        if (ext_x - pos_x) >= 2 and pos_y >= 1:
            boundaries.append(self.NORTHERN4)

        # Southern directions
        if pos_x >= 1 and (ext_y - pos_y) >= 2:
            boundaries.append(self.SOUTHERN1)
        if (ext_x - pos_x) >= 1 and (ext_y - pos_y) >= 2:
            boundaries.append(self.SOUTHERN2)
        if (ext_x - pos_x) >= 2 and (ext_y - pos_y) >= 1:
            boundaries.append(self.SOUTHERN3)
        if pos_x >= 2 and (ext_y - pos_y) >= 1:
            boundaries.append(self.SOUTHERN4)

        return boundaries

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

        pos = (pos_x, pos_y)
        self.boundaries = self.prepare_boundaries(board, pos_x, pos_y)
        self.prepare_adj(board, pos_x, pos_y)

        for direction in self.boundaries:
            logging.info("Knight type movement detected, proceding to unary limits")
            logging.debug("Checking zone for direction %d", direction)
            # Verify all the possible direction adjacencies
            if self.check_zone(direction, board, pos):
                return True

        return False

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
