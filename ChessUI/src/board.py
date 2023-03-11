from const import *
from piece import *
from square import Square
from sound import Sound
from move import Move
import copy
import os

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move, isCheck, testing=False):
        initial = move.initial
        final = move.final

        toPlay = "move.mp3"

        if self.squares[final.row][final.col].piece != None:
            toPlay = "capture.mp3"


        en_passant_empty = self.squares[final.row][final.col].isempty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(
                        os.path.join('../assets/sounds/capture.wav'))
                    sound.play()
            
            # pawn promotion
            else:
                self.check_promotion(piece, final)

        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                if diff < 0:
                    rook = piece.left_rook
                    self.move(rook, Move(Square(initial.row, 0), Square(initial.row, 3)), False)
                else:
                    rook = piece.right_rook
                    self.move(rook, Move(Square(initial.row, 7), Square(initial.row, 5)), False)
                toPlay = "castle.mp3"

        if isCheck == True:
            toPlay = "move-check.mp3"

        sound = Sound(
            os.path.join('../assets/sounds/'+toPlay))
        sound.play()
                

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def _create(self):
            for row in range(ROWS):
                for col in range(COLS):
                    self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        rook_left = Rook(color)
        rook_right = Rook(color)
        self.squares[row_other][0] = Square(row_other, 0, rook_left)
        self.squares[row_other][7] = Square(row_other, 7, rook_right)

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        king = King(color)
        king.left_rook = rook_left
        king.right_rook = rook_right
        self.squares[row_other][4] = Square(row_other, 4, king)
