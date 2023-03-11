import os
import threading
import time
from chess_engine import *
from progress.bar import IncrementalBar   

print("Welcome to the engine analyser.")
#print("Insert the file location for the engine you would like to use!")
#file = input("> ")
#if not os.path.isfile(file):
#    os.system('exit')

engine = Engine("Stockfish 15.1\\stockfish-windows-2022-x86-64-avx2")
if engine.has_configuration("Hash"):
    engine.set_engine_configuration("Hash", 4096)
engine.set_engine_configuration("Threads", 4)

print("Insert the location for the game's PGN file.")
file = input("> ")
if not os.path.isfile(file):
    os.system('exit')

game, moves = engine.ChessController.read_pgn(file)

def moveReport():
    bar = IncrementalBar('Game Analysis:', max=moves)
    currMove = 0
    bar.start()
    while engine.analysed_moves < moves:
        if engine.analysed_moves == currMove:
            continue
        currMove += 1
        bar.index = currMove
        bar.update()
        time.sleep(.05)
    bar.finish()

#threading.Thread(target=moveReport).start()
analysis = engine.analyse_pgn(file, depth=15, progress_bar=True)

print("Done! Display analysis?")
show = input("> ")
if show == '' or show == 'y':
    engine.ChessController.make_command_line_analysis_display(analysis, True)