# import string
# import random
# import os
# import sys
# import time
import itertools
from IPython.display import clear_output
from typing import List, Tuple, Optional

# ----------------------------------------------------------------
# ----------------------------------------------------------------

def ChessBoardSetup() -> dict:
    # initialize and return a chess board - create a 2D 8x8 array that has the value for each cell
    # USE the following characters for the chess pieces - lower-case for BLACK and upper-case for WHITE
    # . for empty board cell
    # p/P for pawn
    # r/R for rook
    # t/T for knight
    # b/B for bishop
    # q/Q for queen
    # k/K for king

    board: dict = {

        f'{char}{i + 1}': None
        for char, i in itertools.product( 'abcdefgh', range(8) )

    }

    # set the initial position of the pieces

    board[ 'a1' ] = 'R'
    board[ 'b1' ] = 'T'
    board[ 'c1' ] = 'B'
    board[ 'd1' ] = 'Q'
    board[ 'e1' ] = 'K'
    board[ 'f1' ] = 'B'
    board[ 'g1' ] = 'T'
    board[ 'h1' ] = 'R'

    for char in 'abcdefgh':
        board[ f'{char}2' ] = 'P'

    board[ 'a8' ] = 'r'
    board[ 'b8' ] = 't'
    board[ 'c8' ] = 'b'
    board[ 'd8' ] = 'q'
    board[ 'e8' ] = 'k'
    board[ 'f8' ] = 'b'
    board[ 'g8' ] = 't'
    board[ 'h8' ] = 'r'

    i = 1
    for char in 'abcdefgh':
        board[ f'{char}7' ] = 'p'


    return board
    
def DrawBoard( board: dict, custom_print: dict = None ) -> None:
    # write code to print the board - following is one print example
    # r t b q k b t r
    # p p p p p p p p
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # P P P P P P P P
    # R T B Q K B T R

    print( '    a b c d e f g h' )
    print( '    +-------------+' )
    
    for row in range(8, 0, -1):
        print( f'{row} | ', end='' )
        
        for col in 'abcdefgh':
            index: str = f'{col}{row}'
            piece = board.get( index )
            
            if custom_print is not None and piece is None:
                piece = custom_print.get( index )
            
            if piece is None:
                piece = '.'
                
            print( piece, end=' ' )
            
        print( '' )

def get_piece_position( piece: str, board: dict ) -> ( str | None ):
    if piece.lower() == 'p':
        return None

    return board.get( board.keys()[ board.values().index( piece ) ] )

def MovePiece( piece: str, coord: str, board: dict ):
    # write code to move the one chess piece
    # you do not have to worry about the validity of the move - this will be done before calling this function
    # this function will at least take the move (from-piece and to-piece) as input and return the new board layout
    
    current_position: str = get_piece_position( piece, board )

    board[ current_position ] = None
    board[ coord ] = piece

# ----------------------------------------------------------------

chessboard = ChessBoardSetup()
DrawBoard( chessboard )

# ----------------------------------------------------------------
print()
# ----------------------------------------------------------------

def find_distance( move_from: str, move_to: str ) -> Tuple[ int, int ]:
    return int( move_to[1] ) - int( move_from[1] ), ord( move_to[0] ) - ord( move_from[0] )

def is_path_clear( move_from: str, move_to: str, board: dict, custom_print_dict: dict = None ) -> Optional[ Tuple[ str , str ] ]:

    row_diff, col_diff = find_distance( move_from, move_to )

    row_dir = row_diff
    col_dir = col_diff

    if row_diff != 0:
        row_dir = 1 if min( 0, row_diff ) == 0 else -1

    if col_diff != 0:
        col_dir = 1 if min( 0, col_diff ) == 0 else -1

    col_move: str = chr( ord( move_from[0] ) + col_dir )
    row_move: str = f'{ int( move_from[1] ) + row_dir }'

    next_move: str = f'{ col_move }{ row_move }'

    print( f'{ move_from } -> { next_move }' )

    if row_diff + col_diff == 0:
        return None

    if board.get( next_move ) is not None:
        return next_move, board.get( next_move )

    if custom_print_dict is not None:
        custom_print_dict[ move_from ] = '-'
        custom_print_dict[ next_move ] = '-'

    is_path_clear( next_move, move_to, board, custom_print_dict ) is None
        
# ----------------------------------------------------------------

print_dict = {}
print( is_path_clear( 'a2', 'h7', chessboard, print_dict ) )
DrawBoard( chessboard, print_dict )

print()

print_dict = {}
print( is_path_clear( 'a7', 'h2', chessboard, print_dict ) )
DrawBoard( chessboard, print_dict )

print()

print_dict = {}
print( is_path_clear( 'g3', 'a3', chessboard, print_dict ) )
DrawBoard( chessboard, print_dict )

print()

print_dict = {}
print( is_path_clear( 'b5', 'b1', chessboard, print_dict ) )
DrawBoard( chessboard, print_dict )

print()

print_dict = {}
print( is_path_clear( 'd1', 'd4', chessboard, print_dict ) )
DrawBoard( chessboard, print_dict )

# ----------------------------------------------------------------
print()
# ----------------------------------------------------------------

def IsMoveLegal( piece: str, move_from: str, move_to: str, board: dict ) -> bool:

    # input is from-square and to-square
    # use the input and the board to get the from-piece and to-piece

    if move_from == move_to:
        return False

    if move_from[0] not in 'abcdefgh' or move_from[1] not in '12345678':
        return False

    # If destination is occupied and is friendly
    if board.get( move_to ) is not None and ( board.get( move_to ).isupper() == piece.isupper() ):
        return False

    row_diff, col_diff = find_distance( move_from, move_to, board )

    # Pawn
    if piece.lower() == 'p':

        # Check if out of pawns movement range
        if abs( row_diff * col_diff ) > 2:
            return False

        # If Attacking Diagonally
        if col_diff != 0:

            if abs( row_diff ) > 1:
                return False

            # Destination must not be vacant nor friendly
            return (
                board.get( move_to ) is not None
                and board.get( move_to ).isupper() != piece.isupper()
            )

        # If 2-step move
        if abs( row_diff ) == 2:

            if piece == 'P' and move_from[1] != '2':
                return False

            if move_from[1] != '7':
                return False

    # sourcery skip: merge-nested-ifs
    # Rook
    if piece.lower() == 'r':
        
        if row_diff * col_diff != 0:
            return False
    
    # Bishop - Check if both directions and steps equally in both
    if piece.lower() == 'b':
        
        if row_diff * col_diff != 0:
            return False
    
        if row_diff == col_diff:
            return False
    
    # Queen - Check if either stepping diagonally or in a straight line
    if piece.lower() == 'q':
        
        if row_diff * col_diff != 0 and row_diff != col_diff:
            return False
    
    if piece.lower() == 't':
        
        if row_diff * col_diff == 0:
            return False
        
        if abs( row_diff ) + abs( col_diff ) != 3:
            return False    

    # King
    if piece.lower() == 'k':
        
        if abs( row_diff ) * abs( col_diff ) != 1:
            return False

    return is_path_clear( move_from, move_to, board ) is None

# gets a list of legal moves for a given piece
# input = from-square
# output = list of to-square locations where the piece can move to
def GetListOfLegalMoves():
    pass
    # input is the current player and the given piece as the from-square
    # initialize the list of legal moves, i.e., to-square locations to []
    # go through all squares on the board
    # for the selected square as to-square
        # call IsMoveLegal() with input as from-square and to-square and save the returned value
        # if returned value is True
            # call DoesMovePutPlayerInCheck() with input as from-square and to-square and save the returned value
            # if returned value is False
                # append this move (to-square) as a legal move
    # return the list of legal moves, i.e., to-square locations



# gets a list of all pieces for the current player that have legal moves
def GetPiecesWithLegalMoves():
    pass
    # initialize the list of pieces with legal moves to []
    # go through all squares on the board
    # for the selected square
        # if the square contains a piece that belongs to the current player's team
            # call GetListOfLegalMoves() to get a list of all legal moves for the selected piece / square
            # if there are any legel moves
                # append this piece to the list of pieces with legal moves
    # return the final list of pieces with legal moves



# returns True if the current player is in checkmate, else False
def IsCheckmate():
    pass
    # call GetPiecesWithLegalMoves() to get all legal moves for the current player
    # if there is no piece with any valid move
        # return True
    # else
        # return False



# returns True if the given player is in Check state
def IsInCheck():
    pass
    # find given player's King's location = king-square
    # go through all squares on the board
        # if there is a piece at that location and that piece is of the enemy team
            # call IsMoveLegal() for the enemy player from that square to the king-square
            # if the value returned is True
                # return True
            # else
                # do nothing and continue
    # return False at the end



# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
def IsClearPath():
    pass
    # given the move (from-square and to-square)

    # if the from and to squares are only one square apart
        # return True
    # else
        # if to-square is in the +ve vertical direction from from-square
            # new-from-square = next square in the +ve vertical direction
        # else if to-square is in the -ve vertical direction from from-square
            # new-from-square = next square in the -ve vertical direction
        # else if to-square is in the +ve horizontal direction from from-square
            # new-from-square = next square in the +ve horizontal direction
        # else if to-square is in the -ve horizontal direction from from-square
            # new-from-square = next square in the -ve horizontal direction
        # else if to-square is in the SE diagonal direction from from-square
            # new-from-square = next square in the SE diagonal direction
        # else if to-square is in the SW diagonal direction from from-square
            # new-from-square = next square in the SW diagonal direction
        # else if to-square is in the NE diagonal direction from from-square
            # new-from-square = next square in the NE diagonal direction
        # else if to-square is in the NW diagonal direction from from-square
            # new-from-square = next square in the NW diagonal direction

    # if new-from-square is not empty
        # return False
    # else
        # return the result from the recursive call of IsClearPath() with the new-from-square and to-square



# makes a hypothetical move (from-square and to-square)
# returns True if it puts current player into check
def DoesMovePutPlayerInCheck():
    pass
    # given the move (from-square and to-square), find the 'from-piece' and 'to-piece'
    # make the move temporarily by changing the 'board'
    # Call the IsInCheck() function to see if the 'player' is in check - save the returned value
    # Undo the temporary move
    # return the value saved - True if it puts current player into check, False otherwise



