import pygame
import sys
import os
import threading
import time

rows = ["a", 'b', 'c', 'd', 'e', 'f', 'g', 'h']
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from chess_engine import Engine

from const import *
from game import Game
from square import *
from move import Move

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

def test(main, analysis):

    for item in analysis.analysis:
        time.sleep(2)
        print(item)
        print(item['played_move'][:2])
        moveFrom = item['played_move'][:2]
        moveTo = item['played_move'][2:4]

        row = int(rows.index(moveFrom[0]))
        col = int(moveFrom[1])

        
        row1 = int(rows.index(moveFrom[0]))
        col1 = int(moveFrom[1])
        row2 = int(rows.index(moveTo[0]))
        col2 = int(moveTo[1])

        piece = main.game.board.squares[row][col].piece

        main.game.board.move(piece, Move(Square(row1, col1), Square(row2, col2)))


if __name__ == "__main__":

    engine = Engine("../../Stockfish 15.1\\stockfish-windows-2022-x86-64-avx2")
    if engine.has_configuration("Hash"):
        engine.set_engine_configuration("Hash", 4096)
    engine.set_engine_configuration("Threads", 4)
    analysis = engine.analyse_pgn("../../Game.pgn", depth=10, progress_bar=True)
    main = Main('')
    threading.Thread(target=test, args=(main,analysis,)).start()
    main.loop()