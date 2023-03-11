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


prevMove = ""
def test(main, analysis):

    global prevMove

    for item in analysis.analysis:
        time.sleep(.5)

        if item['played_move'] == prevMove:
            return
        else:
            prevMove = item['played_move']
        
        moveFrom = item['played_move'][:2]
        moveTo = item['played_move'][2:4]

        row = 7 - (int(moveFrom[1]) - 1)
        col = (rows.index(moveFrom[0]))

        row1 = 7 - (int(moveFrom[1]) - 1)
        col1 = (rows.index(moveFrom[0]))
        row2 = 7 - (int(moveTo[1]) - 1)
        col2 = (rows.index(moveTo[0]))

        piece = main.game.board.squares[row][col].piece

        symbol = item['played_move'][len(item['played_move']) - 1]

        main.game.board.move(piece, Move(Square(row1, col1), Square(row2, col2)), (symbol == "+") or (symbol == "#"))


if __name__ == "__main__":

    engine = Engine("../../Stockfish 15.1\\stockfish-windows-2022-x86-64-avx2")
    if engine.has_configuration("Hash"):
        engine.set_engine_configuration("Hash", 4096)
    engine.set_engine_configuration("Threads", 4)
    analysis = engine.analyse_pgn("../../Game.pgn", depth=10, progress_bar=True)
    main = Main('')
    threading.Thread(target=test, args=(main,analysis,)).start()
    main.loop()