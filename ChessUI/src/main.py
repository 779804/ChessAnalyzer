import pygame
import sys

from const import *
from game import Game

class Main:

    def __init__(self, pgn) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode( (1200, HEIGHT) )
        self.screen.fill((20, 20, 20))
        pygame.display.set_caption("Chess Analysis")
        self.game = Game()
        self.pgn = pgn

    def loop(self):

        screen = self.screen
        game = self.game
        board = self.game.board

        while True:
            game.show_bg(screen)
            game.show_pieces(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
                
            pygame.display.update()

if __name__ == "__main__":
    main = Main('')
    main.loop()