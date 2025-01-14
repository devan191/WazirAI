import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:

    def __init__(self):

        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        
    
    # blit methods

    def show_panel(self,surface):
        title_font = pygame.font.Font('assets/font/Pixeltype.ttf', 75)
        text_font = pygame.font.SysFont('MONOSPACE',24, bold = True)
        text1 = title_font.render('Welcome', False, 'White')
        text2 = title_font.render('To', False, 'White')
        text3 = title_font.render('PyChess!', False, 'White')
        text4 = text_font.render('This is 2v2 player mode',True, 'Blue')
        rect = (800, 0, 400, 800)
        #blit
        pygame.draw.rect(surface,'black', rect)
        surface.blit(text1, (900,100))
        surface.blit(text2, (950,150))
        surface.blit(text3, (900,200))
        surface.blit(text4, (850,300))

    def show_bg(self,surface):
        theme = self.config.theme 

        for row in range(ROWS):
            for col in range(COLS):
                #color
                color = theme.bg.light if (row+col) %2 == 0 else theme.bg.dark
                #rect
                rect = (col* SQSIZE, row* SQSIZE, SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)

                #row coordinates
                if col == 0:
                    #color
                    color = theme.bg.dark if row %2 == 0 else theme.bg.light
                    #label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    #blit
                    surface.blit(lbl, lbl_pos)

                #col coordinates
                if row == 7:
                    #color
                    color = theme.bg.light if col %2 == 0 else theme.bg.dark
                    #label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col*SQSIZE + (SQSIZE - 20), COLS*SQSIZE - 20)
                    #blit
                    surface.blit(lbl, lbl_pos)

    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                #piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    #all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        
                        img = pygame.image.load(piece.texture).convert_alpha()
                        img_center = col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self,surface):
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop all the valid moves
            for move in piece.possible_moves:
                #color
                color = theme.moves.light if (move.final.row + move.final.col)%2 == 0 else theme.moves.dark
                #rect
                rect = (move.final.col* SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                #blit 
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
    
            #a move consists of initial square and final square pos
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial,final]:
                #color
                color = theme.trace.light if (pos.row + pos.col)%2 == 0 else theme.trace.dark
                #rect
                rect = (pos.col* SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                #blit 
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.board.hovered_sqr:
            #color
            color = (180,180,180)
            #rect
            rect = (self.board.hovered_sqr.col* SQSIZE, self.board.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            #blit 
            pygame.draw.rect(surface, color, rect, width = 1)

    def change_theme(self):
        self.config.change_theme()
    
    def play_sound(self,captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__()
    
   
    