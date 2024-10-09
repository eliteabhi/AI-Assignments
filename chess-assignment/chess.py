# import string
# import random
# import os
# import sys
# import time
import itertools
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
        custom_print_dict[ move_from ] = '+'
        custom_print_dict[ next_move ] = '+'

    is_path_clear( next_move, move_to, board, custom_print_dict )

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

    row_diff, col_diff = find_distance( move_from, move_to )

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
def GetListOfLegalMoves( player: str, move_from: str, board: dict ) -> Optional[ List ]:

    if 'b' in player.lower():
        player = player.lower()
        row_direction = -1

    else:
        player = player.capitalize()
        row_direction = 1

    if board.get( move_from ) is None or board.get( move_from ).isupper() != player.isupper():
        return None

    piece: str = board.get( move_from )

    move_list = []

    match piece.lower():

        case 'p':

            next_row: str = f'{ int( move_from[1] ) + row_direction }'
            move_list.append(f'{ move_from[0] }{ next_row }')

            next_col: str = f'{ ord( move_from[1] ) + row_direction }'
            move_list.append(f'{ next_col }{ next_row }')

            next_col: str = f'{ ord( move_from[1] ) - row_direction }'
            move_list.append(f'{ next_col }{ next_row }')

            next_row: str = f'{ int( next_row ) + row_direction }'
            move_list.append(f'{ move_from[0] }{ next_row }')

        case 'r':

            move_list.extend(

                f'{ col }{ move_from[1] }'
                for col in 'abcdefgh'
                if col is not move_from[0]

            )

            move_list.extend(

                f'{ move_list[0] }{ row }'
                for row in '12345678'
                if row != int(move_from[1])

            )

        case 'b':

            move_list.extend(

                f'{ col }{ row }'
                for col in 'abcdefgh'
                for row in '12345678'

                if (

                    col is not move_from[0]
                    and row!= int( move_from[1] )
                    and (

                        ( col > move_from[0] and row > move_from[1] )
                        or ( col < move_from[0] and row < move_from[1] )

                    )
                )
            )

        case 'q':

            move_list.extend(
                f'{ col }{ row }'
                for col in 'abcdefgh'
                for row in '12345678'
                if (
                    col is not move_from[0]
                    and row!= int( move_from[1] )
                    and (
                        ( col > move_from[0] and row > move_from[1] )
                        or ( col < move_from[0] and row < move_from[1] )
                    )
                )
            )

            move_list.extend(

                f'{ col }{ move_from[1] }'
                for col in 'abcdefgh'
                if col is not move_from[0]

            )

            move_list.extend(

                f'{ move_list[0] }{ row }'
                for row in '12345678'
                if row != int(move_from[1])

            )

        case 'k':

            move_list.append( f'{ chr( ord( move_from[0]) - 1 ) }{ move_from[1] }' )

            move_list.append( f'{ chr( ord( move_from[0]) + 1 ) }{ move_from[1] }' )

            move_list.append( f'{ move_from[0] }{ chr( int( move_from[1] ) - 1 ) }' )

            move_list.append( f'{ move_from[0] }{ chr( int( move_from[1] ) + 1 ) }' )

        case 't':

            next_col = ord( move_from[0] ) + 1
            next_row = int( move_from[1] ) + 2
            move_list.append( f'{ next_col }{ next_row }' )

            next_col = ord( move_from[0] ) - 1
            move_list.append( f'{ next_col }{ next_row }' )

            next_row = int( move_from[1] ) - 2
            move_list.append( f'{ next_col }{ next_row }' )

            next_col = ord( move_from[0] ) - 1
            move_list.append( f'{ next_col }{ next_row }' )


    legal_moves: Optional[ List ] = [

        move
        for move in move_list
        if IsMoveLegal( player, move_from, move, board )

    ]

    if legal_moves == []:
        legal_moves = None

    return legal_moves

# gets a list of all pieces for the current player that have legal moves
def GetPiecesWithLegalMoves( player: str, board: dict ) -> Optional[ List ]:

    player = player.lower() if 'b' in player.lower() else player.capitalize()

    spaces_with_pieces_with_legal_moves = []

    for space in board:

        if board.get( space ) is None or board.get( space ).isupper() != player.isupper():
            continue

        if GetListOfLegalMoves( player, space, board ) is not None:
            spaces_with_pieces_with_legal_moves.append( space )

    return spaces_with_pieces_with_legal_moves or None

# returns True if the given player is in Check state
def IsInCheck( player: str, board: dict ) -> Optional[ Tuple[ str, str ] ]:

    # Get player's king symbol
    king_symbol: str = 'k' if 'b' in player.lower() else 'K'

    # Find the player's king
    pieces_with_legal_moves: List = GetPiecesWithLegalMoves( player, board )
    king_square: str = pieces_with_legal_moves.pop( 0 )

    while board.get( king_square ) != king_symbol:
        king_square = pieces_with_legal_moves.pop( 0 )

    occupied_spaces: List = []

    # Check if player is in check by rook/queen
    occupied_spaces.append( is_path_clear( king_square, f'a{ king_square[1] }', board ) )

    occupied_spaces.append( is_path_clear( king_square, f'h{ king_square[1] }', board ) )

    occupied_spaces.append( is_path_clear( king_square, f'{ king_square[0] }1', board ) )

    occupied_spaces.append( is_path_clear( king_square, f'{ king_square[0] }8', board ) )

    # Check if player is in check by bishop/queen

    distance_from_top_left = find_distance( king_square, 'a8' )

    min_col: str = chr( ord( 'a' ) + ( distance_from_top_left[1] - distance_from_top_left[0] ) )
    min_row: str = chr( 1 + ( distance_from_top_left[1] - distance_from_top_left[0] ) )

    max_row = chr( ord( 'a' ) + ( distance_from_top_left[0] - distance_from_top_left[1] ) )

    max_top_left: str = f'{ min_col }{ max_row }'

    occupied_spaces.append( is_path_clear( king_square, 'a1', board ) )

    occupied_spaces.append( is_path_clear( king_square, 'h8', board ) )

    occupied_spaces.append( is_path_clear( king_square, 'a8', board ) )

    occupied_spaces.append( is_path_clear( king_square, 'h1', board ) )

    square = occupied_spaces.pop( 0 )

    while len( occupied_spaces ) > 0 and square is not None and square[1].isupper() != king_symbol.isupper():
        return square

    return None

    # find given player's King's location = king-square
    # go through all squares on the board
        # if there is a piece at that location and that piece is of the enemy team
            # call IsMoveLegal() for the enemy player from that square to the king-square
            # if the value returned is True
                # return True
            # else
                # do nothing and continue
    # return False at the end


# makes a hypothetical move (from-square and to-square)
# returns True if it puts current player into check
def DoesMovePutPlayerInCheck():
    pass
    # given the move (from-square and to-square), find the 'from-piece' and 'to-piece'
    # make the move temporarily by changing the 'board'
    # Call the IsInCheck() function to see if the 'player' is in check - save the returned value
    # Undo the temporary move
    # return the value saved - True if it puts current player into check, False otherwise

