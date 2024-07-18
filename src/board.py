from const import *
from square import *
from piece import *
from move import Move
class Board:
    
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self.next_player = 'white'
        self.hovered_sqr = None
        self.moves_log = []
        self.moved_piece_log = []
        self.last_piece_captured = []
        self._create() 
        self._add_pieces('white')
        self._add_pieces('black')  

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        if self.squares[final.row][final.col].isempty():
            self.last_piece_captured.append(0)
        else:
            self.last_piece_captured.append(self.squares[final.row][final.col].piece)

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # move
        piece.moved = True
        self.moves_log.append(move)
        self.moved_piece_log.append(piece)
        # clear valid moves
        piece.clear_moves()

        #set last move
        self.last_move = move

    def possible_move(self, piece, move):
        
        return (move in piece.possible_moves)

    def calc_moves(self, piece, row, col):
        '''
        Calculate all the possible(valid) moves of a specific piece on a specific position
        
        '''
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row+2,col+1),
                (row+1,col+2),
                (row-2,col-1),
                (row-1,col-2),
                (row+2,col-1),
                (row-1,col+2),
                (row-2,col+1),
                (row+1,col-2)
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row,possible_move_col)
                        # create a new move
                        move = Move(initial,final)
                        #append new valid move
                        piece.add_move(move)

        def pawn_moves():
            
            # Steps: 1 step if the pawn has moved, otherwise 2 steps from the initial position
            steps = 1 if piece.moved else 2

            # Vertical moves
            for step in range(1, steps + 1):
                possible_move_row = row + piece.dir * step
                if Square.in_range(possible_move_row):  # Check if row is within board range
                    if self.squares[possible_move_row][col].isempty():
                        # Create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # Create a new move
                        move = Move(initial, final)
                        # Append new move
                        piece.add_move(move)
                    else:
                        break  # Blocked by another piece, stop checking further
                else:
                    break  # Row is out of range, stop checking further

            # Diagonal moves for capturing
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):  # Check if both row and column are within board range
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # Create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # Create a new move
                        move = Move(initial, final)
                        # Append the move
                        piece.add_move(move)

            #en pessiant moves
        
        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row,possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row,possible_move_col)
                        # create a possible new move
                        move = Move(initial, final)

                        #empty cells
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #append new move
                            piece.add_move(move)

                        # has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            #append new move  and break
                            piece.add_move(move)
                            break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            #just break
                            break
                    else:
                        #not in range
                        break
                    # incrementing moves by incr
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1,  col),
                (row+1,  col),
                (row  ,col+1),
                (row  ,col-1),
                (row-1,col+1),
                (row+1,col-1),
                (row+1,col+1),
                (row-1,col-1)
            ]        
            #these are normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row,possible_move_col)
                        # create a new move
                        move = Move(initial,final)
                        #append new valid move
                        piece.add_move(move)
            
            #castling moves

            #queen castling

            #king castling

            
        if isinstance(piece, Pawn): pawn_moves()

        elif isinstance(piece, Knight): knight_moves()

        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1), #up-right
                ( 1,-1), #down-left
                (-1,-1), #up-left
                ( 1, 1)  #down-right
           ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), # up
                ( 1, 0),  # down
                ( 0, 1),  # right
                ( 0,-1)  # left
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1), #up-right
                ( 1,-1), #down-left
                (-1,-1), #up-left
                ( 1, 1),  #down-right
                (-1, 0), # up
                ( 1, 0),  # down
                ( 0, 1),  # right
                ( 0,-1)  # left
            ])

        elif isinstance(piece, King): king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row,col)
        
    def _add_pieces(self,color):

        row_pawn, row_other = (1,0) if color == 'black' else (6,7)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        
        #bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        #King
        self.squares[row_other][4] = Square(row_other, 4, King(color))
    
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.squares[row][col]

    def reset(self):
        self.__init__()

    def undo_move(self):
        if len(self.moves_log) != 0:

            current_move = self.moves_log.pop()
            current_piece = self.moved_piece_log.pop()
            last_capt_piece = self.last_piece_captured.pop()

            if isinstance(current_piece,Pawn):
                if current_piece not in self.moved_piece_log:
                    current_piece.moved = False

            initial = current_move.final
            final = current_move.initial
            move = Move(initial,final)

            # console board move update
            self.squares[initial.row][initial.col].piece = None if last_capt_piece==0 else last_capt_piece
            self.squares[final.row][final.col].piece = current_piece

            self.last_move = move
            self.next_turn()
