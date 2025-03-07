import os
import math
class Piece:

    def __init__(self, name, color, value, texture = None, texture_rect = None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.possible_moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
    
    def __str__(self) -> str:
        return f"{self.color} {self.name}"
    
    def __repr__(self) -> str:
        return f"{self.color} {self.name}"
    
    def set_texture(self,size=80):
        #img url
        self.texture = os.path.join(
            f'assets/images/mimgs-{size}px/{self.color}_{self.name}.png'
        )
    def add_move(self, move):
        self.possible_moves.append(move)

    def clear_moves(self):
        self.possible_moves = []

class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn',color, 1.0)

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight',color, 3.0001)
    
class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop',color, 3.0)

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook',color, 5.0)

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen',color, 9.0)

class King(Piece):

    def __init__(self, color):
        super().__init__('king',color, math.inf)