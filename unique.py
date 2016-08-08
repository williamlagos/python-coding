#!/usr/bin/adj_ython
#
# Unique Combinations adj_ython app
# Author: William Oliveira de Lagos <william.lagos@outlook.com>
#

""" Finds the unique combinations of X pieces on a M x N chessboard """

import sys
import json
import logging
import argparse
import itertools

# 0, 1, 2, 3, 4, 5, 6, 7 are constants to North, East, South, West,
# Northeast, Southeast, South-west and Northwest, respectively.

N = 0
E = 1
S = 2
W = 3
NE = 4
SE = 5
SW = 6
NW = 7

# 0 - free to use
# 1 - threat zone
# Unicode - piece placed

FREE = 0
THREAT = 1

# Position tuple codes
X = 0
Y = 1

def check_nzone(direction, adjacencies, board, pos_x, pos_y):
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

def check_dzone(direction, adjacencies, squares, board, pos):
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

def check_zone(direction, adjacencies, squares, board, pos):
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
            adj_x = pos[X] + (1 * sqr)
            adj_y = pos[Y]
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
    ext = (len(board[0]), len(board))
    is_adjacency_occupied = False
    # Iterate over the available directions and verify if it's
    # viable to put the piece in this position
    sqr = (1, 1, 1, 1)
    for drc, available in enumerate(zone):
        # Verify if this piece can go this direction
        if directions[drc] == 0:
            return
        # Verify if the directions of this piece are just one
        # square per time or the entire row/column
        if directions[drc] > 1:
            sqr = pos[Y] - 1, pos[X] - 1, ext[Y] - pos[Y], ext[X] - pos[X]
        else:
            logging.debug("King type movement detected, proceding to unary limits")
        # Verify all the possible direction adjacencies
        if available is N and check_zone(N, adj, sqr[0], board, pos):
            is_adjacency_occupied = True
        elif available is E and check_zone(E, adj, sqr[1], board, pos):
            is_adjacency_occupied = True
        elif available is S and check_zone(S, adj, sqr[2], board, pos):
            is_adjacency_occupied = True
        elif available is W and check_zone(W, adj, sqr[3], board, pos):
            is_adjacency_occupied = True
        elif available is NE and check_dzone(NE, adj, (sqr[0], sqr[1]), board, pos):
            is_adjacency_occupied = True
        elif available is SE and check_dzone(SE, adj, (sqr[2], sqr[1]), board, pos):
            is_adjacency_occupied = True
        elif available is SW and check_dzone(SW, adj, (sqr[2], sqr[3]), board, pos):
            is_adjacency_occupied = True
        elif available is NW and check_dzone(NW, adj, (sqr[2], sqr[3]), board, pos):
            is_adjacency_occupied = True
        return is_adjacency_occupied


def check_knight_adjacencies(zone, adj, board, pos):
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
    if N in zone and pos[X] >= 2 and check_nzone(N, adj, board, pos[X], pos[Y]):
        is_adjacency_occupied = True
    if S in zone and pos[X] >= 2 and check_nzone(S, adj, board, pos[X], pos[Y]):
        is_adjacency_occupied = True
    if W in zone and pos[Y] >= 2 and check_nzone(W, adj, board, pos[X], pos[Y]):
        is_adjacency_occupied = True
    if E in zone and pos[Y] >= 2 and check_nzone(E, adj, board, pos[X], pos[Y]):
        is_adjacency_occupied = True

    # South directions adjacencies with special extremities
    if W in zone and (ext[X] - pos[Y]) >= 2 and check_nzone(SW, adj, board, pos[X], pos[Y]):
        is_adjacency_occupied = True
    if E in zone and (ext[Y] - pos[Y]) >= 2 and check_nzone(NE, adj, board, pos[X], pos[Y]):
        is_adjacency_occupied = True
    if S in zone and (ext[X] - pos[X]) >= 2 and check_nzone(SE, adj, board, pos[X], pos[Y]):
        is_adjacency_occupied = True
    if N in zone and (ext[X] - pos[X]) >= 2 and check_nzone(NW, adj, board, pos[X], pos[Y]):
        is_adjacency_occupied = True

    return is_adjacency_occupied

def verify_adjacents(typ, board, pos_x, pos_y):
    """

    Verify the adjacencies of the square that the
    piece will be put.

    Keyword arguments:

    typ -- Type of the chess piece
    board -- The chessboard matrix with integer codes
    pos_x -- X position on the chessboard to put the piece
    pos_y -- Y position on the chessboard to put the piece

    """

    both = 0
    ext = (len(board[0]), len(board))
    adj, zone, available_zone = [], [], []
    # It doesn't need to verify the upper or down directions if we are on extremity
    if pos_y == 0:
        zone = [3, 6, 2, 5, 1]
    elif pos_y == ext[Y]:
        zone = [3, 7, 0, 4, 1]
    # If the square is in the middle, all the vertical adjacencies will be checked
    else:
        zone = [3, 6, 7, 0, 2, 4, 5, 1]
        both += 1

    # Verify if the square isn't on the horizontal extremities
    if pos_x == 0:
        available_zone = zone[2 + both:]
    elif pos_x == ext[Y]:
        available_zone = zone[:-2 - both]
    logging.debug("Verified existing limits on board and possible directions: %s", available_zone)

    # A fixed dict with the movements of each piece are stored in a file called unique.json.
    cfg = open('unique.json', 'r')
    movements = json.load(cfg)
    logging.debug("Checked possible movements of piece of type %s: %s", typ, movements[typ])

    # Special adjacencies for the knight movement
    if sum(movements[typ]) == 0:
        logging.debug("Knight type movement detected, proceding to special limits")
        if check_knight_adjacencies(available_zone, adj, board, (pos_x, pos_y)):
            return []
    else:
        logging.debug("Normal type movement detected, proceding to normal limits")
        if check_adjacencies(available_zone, movements[typ], adj, board, (pos_x, pos_y)):
            return []
    # If the function didn't return until this point,
    # it's possible to put the piece in x, y coordinate
    logging.debug("All adjancencies are valid, proceding to deliver to unique_configuration()")
    return adj

def put_piece(adjacencies, piece, board, pos_x, pos_y):
    """

    Put the given piece in the board with its adjacencies included.

    Keyword arguments:

    adjacencies -- List of adjacencies of the piece
    piece -- The letter of the piece that will be inserted
    board -- Main matrix chessboard to be manipulated
    x -- X position of the given piece
    y -- Y position of the given piece

    """
    logging.debug("Board before insertion of %s in (%d, %d): %s", piece, pos_x, pos_y, board)
    # Put the piece with the unicode representation on board
    board[pos_x][pos_y] = ord(piece)

    logging.debug("List of adjacencies of %s for (%d, %d): %s", piece, pos_x, pos_y, adjacencies)
    # Insert all the adjacencies related to the piece
    for pos_x, pos_y in adjacencies:
        board[pos_x][pos_y] = THREAT
    logging.debug("Board after insertion of %s in (%d, %d): %s", piece, pos_x, pos_y, board)

def unique_configuration(sequence, board):
    """

    Search for a unique configuration for a given
    sequence of pieces on a chessboard with given
    dimensions.

    Keyword arguments:

    sequence -- A permutated sequence of pieces
    board -- The chessboard matrix with integer codes

    """

    adjacencies = []
    # Verify if there is more piece to put in the board
    if len(sequence) > 0:
        piece = sequence[0]
        for pos_y, row in enumerate(board):
            for pos_x, square in enumerate(row):
                # Verify if the position has threat or piece placed
                if square != 0:
                    continue
                # Verify if the adjacencies of the position are available
                adjacencies = verify_adjacents(piece, board, pos_x, pos_y)
                if not adjacencies:
                    continue
                logging.debug("Putting piece %s on board", piece)
                put_piece(adjacencies, piece, board, pos_x, pos_y)

    # If not, the function returns its recursive call
    else:
        return
    unique_configuration(sequence[1:], board)

def possible_ordered_sequences(pieces):
    """

    Create all permutations of the given list of the
    pieces, then return in a list of pieces tuple.

    Keyword arguments:

    pieces -- The pieces dictionary with the quantity of each piece.
    """

    sequence, sequences = [], []

    # Iterate over the pieces original dict
    for piece, number in pieces.items():
        if number < 1:
            continue
        times = (("%s " % piece)*number)
        sequence.extend(times.split())

    # Create permutations with itertools.permutations, then return a set of it
    sequences.extend(itertools.permutations(sequence))
    return set(sequences)

def main():
    """

    Application main function. It doesn't receive
    arguments by the function, only by the parser.

    """

    # Configures the logging processor for information
    logging.basicConfig(filename='unique.log', level=logging.DEBUG)

    # Configures the argument parser for the input
    parser = argparse.ArgumentParser(
        description="Find unique configurations of a M x N chessboard.")
    parser.add_argument('-m', type=int, default=0, help="Number of horizontal rows")
    parser.add_argument('-n', type=int, default=0, help="Number of vertical columns")
    parser.add_argument('-K', type=int, default=0, help="King piece quantity, default is 0")
    parser.add_argument('-Q', type=int, default=0, help="Queen piece quantity, default is 0")
    parser.add_argument('-R', type=int, default=0, help="Rook piece quantity, default is 0")
    parser.add_argument('-B', type=int, default=0, help="Bishop piece quantity, default is 0")
    parser.add_argument('-N', type=int, default=0, help="Knight piece quantity, default is 0")
    args = parser.parse_args()
    pieces = vars(args)

    # Verify if there is a valid size for the chessboard
    if args.m < 3 or args.n < 3:
        sys.exit("Invalid size for the board, it must be 3 x 3 or bigger.")
    row, col = pieces.pop('m'), pieces.pop('n')

    # Verify if there is any piece to test with
    quantity = args.K + args.Q + args.R + args.B + args.N
    if quantity < 2:
        sys.exit("There isn't enought pieces for combinations, it must be 2 or more.")

    logging.info("Total number of pieces: %d", quantity)
    logging.info("Relation of pieces for the combination: %s", pieces)
    logging.info("Chessboard dimensions - Rows: %d Columns: %d", row, col)

    # Generate a list of possible alternative of ordered pieces
    permutations = possible_ordered_sequences(pieces)
    logging.info("Sequence of possible permutations: %s", permutations)

    # Generate the board matrix with zeros and call recursive function for unique configurations
    board = [[0] * col for _ in itertools.repeat(None, row)]
    for sequence in permutations:
        unique_configuration(sequence, board)

    # print(board)

if __name__ == "__main__":
    try:
        main()
    except SystemExit, err:
        # This log will include content written in sys.exit
        logging.exception("Unique has failed with exception")
        logging.error(str(err))
        raise
