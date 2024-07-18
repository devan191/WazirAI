import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()
        self.clock = pygame.time.Clock()
        self.is_update_needed = True  # Initialize the update needed flag

    def mainloop(self):
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board

        while True:
            self.handle_events(screen)

            # Only update the game display if something changes
            if dragger.dragging or self.is_update_needed:
                self.display_game(screen)

            # Cap the frame rate at 60 FPS
            self.clock.tick(60)
            pygame.display.update()

    
    def handle_events(self,screen):
        dragger = self.game.dragger
        board = self.game.board

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            #key press
            if event.type == pygame.KEYDOWN:
                #changing themes
                if event.key == pygame.K_t:
                    self.game.change_theme()
                    self.is_update_needed = True
                
                if event.key == pygame.K_r:
                    board.reset()
                    self.is_update_needed = True
                
                if event.key == pygame.K_b:
                    if len(board.moves_log) == 1:
                        board.reset()
                        self.is_update_needed = True
                    else:
                        board.undo_move()
                        self.is_update_needed = True
                    
            #dragging/ hovering
            if event.type == pygame.MOUSEMOTION:
                motion_row = event.pos[1] // SQSIZE
                motion_col = event.pos[0] // SQSIZE
                if(motion_row < 0): motion_row = 0
                if(motion_row > 7): motion_row = 7
                if(motion_col < 0): motion_col = 0
                if(motion_col > 7): motion_col = 7
                board.set_hover(motion_row, motion_col)
                self.is_update_needed = True

                if dragger.dragging:
                    dragger.update_mouse(event.pos)
                    self.is_update_needed = True

            #click
            if event.type == pygame.MOUSEBUTTONDOWN and self.game.flag:
                dragger.update_mouse(event.pos)
                clicked_row = dragger.mouseY // SQSIZE
                clicked_col = dragger.mouseX // SQSIZE

                if board.squares[clicked_row][clicked_col].has_piece():
                    
                    piece = board.squares[clicked_row][clicked_col].piece
                    #valid piece color ?
                    if piece.color == board.next_player:
                        board.calc_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        self.is_update_needed = True
                        self.game.flag = False

            #click release
            if event.type == pygame.MOUSEBUTTONUP and dragger.dragging:
                
                dragger.update_mouse(event.pos)
                released_row = dragger.mouseY // SQSIZE
                released_col = dragger.mouseX // SQSIZE

                initial = Square(dragger.initial_row, dragger.initial_col)
                final = Square(released_row, released_col)
                move = Move(initial, final)

                if board.possible_move(dragger.piece, move):
                    captured = board.squares[released_row][released_col].has_piece()

                    board.move(dragger.piece, move)
                    #sound
                    self.game.play_sound(captured)
                    #setting up next player's turn
                    board.next_turn()

                dragger.piece.clear_moves()    # this was the nasty bug... moves of piece were not clearing if it was an invalid move
                dragger.undrag_piece()
                self.game.flag = True
                self.is_update_needed = True

    def display_game(self, screen):
        self.game.show_bg(screen)
        self.game.show_last_move(screen)
        self.game.show_moves(screen)
        self.game.show_pieces(screen)
        self.game.show_hover(screen)
        if self.game.dragger.dragging:
            self.game.dragger.update_blit(screen) 
        self.is_update_needed = False

if __name__ == "__main__":
    main = Main()
    main.mainloop()
