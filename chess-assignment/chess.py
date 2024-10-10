# import string
import random
# import os
# import sys
# import time
import itertools
from copy import deepcopy
from typing import List, Tuple, Optional, Callable, Any

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

def MovePiece( move_to: str, board: dict, move_from: str = None, piece: str = None ) -> Optional[ str ]:
    # write code to move the one chess piece
    # you do not have to worry about the validity of the move - this will be done before calling this function
    # this function will at least take the move (from-piece and to-piece) as input and return the new board layout

    if piece is None:
        piece: str = board.get( move_from )

        if move_from is None:
            return

    else:
        move_from: str = get_piece_position( piece, board )

    captured_piece: str = board.get( move_to )

    board[ move_to ] = piece
    board[ move_from ] = None

    return captured_piece

# ----------------------------------------------------------------

chessboard = ChessBoardSetup()
DrawBoard( chessboard )

# ----------------------------------------------------------------
print()
# ----------------------------------------------------------------

def find_distance( move_from: str, move_to: str ) -> Tuple[ int, int ]:
    return int( move_to[1] ) - int( move_from[1] ), ord( move_to[0] ) - ord( move_from[0] )

def is_path_clear( move_from: str, move_to: str, board: dict, custom_print_dict: dict = None, print_path: bool = False ) -> Optional[ Tuple[ str , str ] ]:

    if move_from[0] not in 'abcdefgh' or move_to[0] not in 'abcdefgh':
        return None

    if move_from[1] not in '12345678' or move_to[1] not in '12345678':
        return None

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

    if print_path:
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
print( is_path_clear( 'a2', 'h7', chessboard, print_dict, True ) )
DrawBoard( chessboard, print_dict )

print()

print_dict = {}
print( is_path_clear( 'a7', 'h2', chessboard, print_dict, True ) )
DrawBoard( chessboard, print_dict )

print()

print_dict = {}
print( is_path_clear( 'g3', 'a3', chessboard, print_dict, True ) )
DrawBoard( chessboard, print_dict )

print()

print_dict = {}
print( is_path_clear( 'b5', 'b1', chessboard, print_dict, True ) )
DrawBoard( chessboard, print_dict )

print()

print_dict = {}
print( is_path_clear( 'd1', 'd4', chessboard, print_dict, True ) )
DrawBoard( chessboard, print_dict )

# ----------------------------------------------------------------
print()
# ----------------------------------------------------------------

# returns True if the given player is in Check state
def IsInCheck( player: str, board: dict ) -> Optional[ Tuple[ str, str ] ]:

    # Get player's king symbol
    king_symbol: str = 'k' if 'b' in player.lower() else 'K'

    # Find the player's king
    all_pieces: List = list( board.keys() )
    king_square: str = all_pieces.pop( 0 )

    while all_pieces and board.get( king_square ) != king_symbol:
        king_square = all_pieces.pop( 0 )

    occupied_spaces: List = []

    # Check if player is in check by rook/queen

    occupied_spaces.append( is_path_clear( king_square, f'a{ king_square[1] }', board ) )
    occupied_spaces.append( is_path_clear( king_square, f'h{ king_square[1] }', board ) )
    occupied_spaces.append( is_path_clear( king_square, f'{ king_square[0] }1', board ) )
    occupied_spaces.append( is_path_clear( king_square, f'{ king_square[0] }8', board ) )

    # Check if player is in check by bishop/queen

    distance_from_top_left = find_distance( king_square, 'a8' )
    distance_from_top_right = find_distance( king_square, 'h8' )
    distance_from_bottom_left = find_distance( king_square, 'a1' )
    distance_from_bottom_right = find_distance( king_square, 'h1' )

    col: str = chr( max( ord( 'a' ), ord( 'a' ) + ( distance_from_top_left[1] - distance_from_top_left[0] ) ) )
    row: str = min( 8, 8 - ( distance_from_top_left[0] + distance_from_top_left[1] ) )

    if distance_from_top_left[0] == 0:
        top_left = king_square

    top_left: str = f'{ col }{ row }'

    col: str = chr( min( ord( 'h' ), ord( 'h' ) - ( distance_from_top_right[1] - distance_from_top_right[0] ) ) )
    row: str = min( 8, 8 - ( distance_from_top_right[0] - distance_from_top_right[1] ) )

    if distance_from_top_left[0] == 0:
        top_left = king_square

    top_right: str = f'{ col }{ row }'

    col: str = chr( min( ord( 'h' ), ord( 'h' ) - ( distance_from_bottom_right[1] + distance_from_bottom_right[0] ) ) )
    row: str = max( 1, 1 + ( distance_from_bottom_right[0] - distance_from_bottom_right[1] ) )

    bottom_right: str = f'{ col }{ row }'

    col: str = chr( max( ord( 'a' ), ord( 'a' ) + ( distance_from_bottom_left[0] - distance_from_bottom_left[1] ) ) )
    row: str = max( 1, 1 + ( distance_from_bottom_left[1] - distance_from_bottom_left[0] ) )

    bottom_left: str = f'{ col }{ row }'

    diagonals: str = [ bottom_left, bottom_right, top_left, top_right ]

    for space in diagonals:
        path = is_path_clear( king_square, space, board )
        if path is not None and path[1].lower() in [ 'b', 'q', 'p' ]:
            occupied_spaces.append( path )

    # Check if player is in check by pawn

    spaces = occupied_spaces
    for square in spaces:

        if square is None:
            continue

        row_diff, col_diff = find_distance( king_square, square[0] )
        if square[1] == 'p' and ( row_diff != 1 or col_diff not in [ -1, 1 ] ):
            occupied_spaces.remove( square )

        elif square[1] == 'P' and ( row_diff != -1 or col_diff not in [ -1, 1 ] ):
            occupied_spaces.remove( square )

    # Check if player is in check by a knight

    top_left = f' { chr( ord( king_square[0] ) - 1 ) }{ int( king_square[1] ) + 2 }'
    top_right = f' { chr( ord( king_square[0] ) - 1 ) }{ int( king_square[1] ) + 2 }'
    bottom_left = f' { chr( ord( king_square[0] ) - 1 ) }{ int( king_square[1] ) + 2 }'
    bottom_right = f' { chr( ord( king_square[0] ) - 1 ) }{ int( king_square[1] ) + 2 }'

    occupied_spaces.append( is_path_clear( king_square, top_left, board ) )
    occupied_spaces.append( is_path_clear( king_square, top_right, board ) )
    occupied_spaces.append( is_path_clear( king_square, bottom_left, board ) )
    occupied_spaces.append( is_path_clear( king_square, bottom_left, board ) )

    square = occupied_spaces.pop( 0 )

    while len( occupied_spaces ) > 0 and ( square is None or square[1].isupper() == king_symbol.isupper() ):
        square = occupied_spaces.pop( 0 )

    if square is not None and square[1].isupper() == king_symbol.isupper():
        square = None

    return square or None

# makes a hypothetical move (from-square and to-square)
# returns True if it puts current player into check
def DoesMovePutPlayerInCheck( player: str, move_from: str, move_to: str, board: dict ) -> bool:

    mock_board: dict = deepcopy( board )

    MovePiece( move_from=move_from, move_to=move_to, board=mock_board )

    return IsInCheck( player, board ) is not None

#----------------------------------------------------------------
print()
#----------------------------------------------------------------

def IsMoveLegal( move_from: str, move_to: str, board: dict ) -> bool:

    # input is from-square and to-square
    # use the input and the board to get the from-piece and to-piece

    if move_from == move_to:
        return False

    if move_from[0] not in 'abcdefgh' or move_from[1] not in '12345678' or move_to[0] not in 'abcdefgh' or move_to[1] not in '12345678':
        return False

    piece: str = board.get( move_from )

    if piece is None:
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

        else:
            return True

    # King
    if piece.lower() == 'k':

        if abs( row_diff ) * abs( col_diff ) != 1:
            return False

    return is_path_clear( move_from, move_to, board ) is None

# ----------------------------------------------------------------
# ----------------------------------------------------------------

# gets a list of legal moves for a given piece
# input = from-square
# output = list of to-square locations where the piece can move to
def GetListOfLegalMoves( player: str, move_from: str, board: dict ) -> Optional[ List ]:

    if 'b' in player.lower():
        player = player.lower()
        row_direction = -1

    else:
        player = player.upper()
        row_direction = 1

    if board.get( move_from ) is None or board.get( move_from ).isupper() != player.isupper():
        return None

    piece: str = board.get( move_from )

    move_list = []

    match piece.lower():

        case 'p':

            next_row: str = f'{ int( move_from[1] ) + row_direction }'
            move_list.append(f'{ move_from[0] }{ next_row }')

            next_col: str = f'{ chr( ord( move_from[0] ) + row_direction ) }'
            move_list.append(f'{ next_col }{ next_row }')

            next_col: str = f'{ chr( ord( move_from[0] ) - row_direction ) }'
            move_list.append(f'{ next_col }{ next_row }')

            next_row: str = f'{ int( next_row ) + row_direction * 2 }'
            move_list.append(f'{ move_from[0] }{ next_row }')

        case 'r':

            move_list.extend(

                f'{ col }{ move_from[1] }'
                for col in 'abcdefgh'
                if col is not move_from[0]

            )

            move_list.extend(

                f'{ move_from[0] }{ row }'
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

            next_col = chr( ord( move_from[0] ) + 1 )
            next_row = int( move_from[1] ) + 2
            move_list.append( f'{ next_col }{ next_row }' )

            next_col = chr( ord( move_from[0] ) - 1 )
            move_list.append( f'{ next_col }{ next_row }' )

            next_row = int( move_from[1] ) - 2
            move_list.append( f'{ next_col }{ next_row }' )

            next_col = chr( ord( move_from[0] ) - 1 )
            move_list.append( f'{ next_col }{ next_row }' )


    legal_moves: Optional[ List ] = [

        move
        for move in move_list
        if IsMoveLegal( move_from, move, board )

    ]

    if legal_moves == []:
        legal_moves = None

    return legal_moves

# ----------------------------------------------------------------
# ----------------------------------------------------------------

# gets a list of all pieces for the current player that have legal moves
def GetPiecesWithLegalMoves( player: str, board: dict ) -> Optional[ List ]:

    spaces_with_pieces_with_legal_moves = []

    player = player.lower() if 'b' in player.lower() else player.upper()

    check_piece = IsInCheck( player, board )

    for space in board:

        if board.get( space ) is None or board.get( space ).isupper() != player.isupper():
            continue

        if check_piece is not None and board.get( space ).lower() != 'k':
            continue

        if GetListOfLegalMoves( player, space, board ) is not None:
            spaces_with_pieces_with_legal_moves.append( space )

    return spaces_with_pieces_with_legal_moves or None

# ----------------------------------------------------------------
# ----------------------------------------------------------------

def run_game( white_bot_function: Callable[ ..., Optional[ Tuple[ str, str, str ] ] ], black_bot_function: Callable[ ..., Optional[ Tuple[ str, str, str ] ] ], turns: int = None, seed: int = None, board: dict = None ):

    if board is None:
        board = ChessBoardSetup()

    turns: int = 1000000 if turns is None else turns

    for turn in range( turns ):
        white_move = white_bot_function( 'white', board, seed )
        black_move = black_bot_function( 'black', board, seed )

        print( f'\nTurn { turn + 1 }:' )

        if white_move is None:
            print( 'White has no legal moves. Black wins!' )
            break

        if black_move is None:
            print( 'Black has no legal moves. White wins!' )
            break

        print( f'White moved from { white_move[0] } to { white_move[1] }.' )
        if white_move[2] is not None:
            print( f'White captured { white_move[2] }.' )

        print( f'Black moved { black_move[0] } to { black_move[1] }.' )
        if black_move[2] is not None:
            print( f'Black captured { black_move[2] }.' )

        print()

        DrawBoard( board )

        print('\n----------------------------------------------------------------')

# ----------------------------------------------------------------
# ----------------------------------------------------------------

def MakeRandomMove( player: str, board: dict, seed: Any = None ) -> Optional[ Tuple[ str, str, str ] ]:
    # pick a random piece and a random legal move for that piece

    pieces_with_legal_moves: List = GetPiecesWithLegalMoves( player, board )

    if pieces_with_legal_moves is None:
        return None

    rnd = random.Random( seed )

    move_from = rnd.choice( pieces_with_legal_moves )

    possible_moves: str = GetListOfLegalMoves( player, move_from, board )
    move_to: str = possible_moves.pop(0)

    while DoesMovePutPlayerInCheck( player, move_from, move_to, board ):

        if not possible_moves:

            if not pieces_with_legal_moves:
                return None

            pieces_with_legal_moves.remove( move_from )

            move_from = random.choice( pieces_with_legal_moves )
            possible_moves: str = GetListOfLegalMoves( player, move_from, board )

        move_to: str = possible_moves.pop( 0 )

    captured_piece = MovePiece( move_from=move_from, move_to=move_to, board=board )

    return move_from, move_to, captured_piece

# ----------------------------------------------------------------

run_game( white_bot_function=MakeRandomMove, black_bot_function=MakeRandomMove, turns=200, seed=90324, board=chessboard )


# ----------------------------------------------------------------
# ----------------------------------------------------------------

def evaluate_score( player: str, move_to: str, board: str ) -> int:

    PIECE_SCORE_LUT: dict[ str, int ] = { 'p': 1, 'r': 5, 't': 3, 'b': 4, 'q': 10, 'k': 20 }

    sign: int = -1 if 'b' in player.lower() else 1

    piece_at_move: str = board.get( move_to )

    return sign * ( PIECE_SCORE_LUT.get( piece_at_move.lower() ) or 0 )

    # this function will calculate the score on the board, if a move is performed
    # give score for each of piece and calculate the score for the chess board


def GetMinMaxMove():
    pass
    # return the best move for the current player using the MinMax strategy
    # to get the allocated points, searching should be 2-ply (one Max and one Min)

    # Following is the setup for a 2-ply game

    # pieces = GetPiecesWithLegalMoves(curPlayer)
    # for each piece in pieces
        # moves = GetListOfLegalMoves(curPlayer, piece)
        # for move in moves
            # perform the move temporarily
            # enemyPieces = GetPiecesWithLegalMoves(enemyPlayer)
            # for enemyPiece in penemyPiecesieces
                # enemyMoves = GetListOfLegalMoves(enemyPlayer, enemyPiece)
                # for enemyMove in enemyMoves
                    # perform the enemyMove temporarily
                    # res = evl(curPlayer)
                    # update the bestEnemyMove -- this is the MIN player trying to minimize from the 'res' evaluation values
                    # undo the enemyMove
            # update the bestMove -- this is the MAX player trying to maximize from the 'bestEnemyMove' evaluation values
            # undo the move
    # if bestMove found without any doubt, pick that
    # if bestMove not found, pick randomly

    # OPTIONAL -- sometimes automated chess keeps on performing the moves again and again
    # e.g., move king left one square and then move king back - repeat
    # For this you will need to remember the previous move and see if the current best move is not the same and opposite as the previous move
    # If so, pick the second best move instead of the best move


