import os
import threading
import time
from chess_engine import *

print("Welcome to the engine analyser.")
print("Insert the file location for the engine you would like to use!")
file = input("> ")
if not os.path.isfile(file):
    os.system('exit')

engine = Engine(file)
engine.set_engine_configuration("Hash", 4096)
engine.set_engine_configuration("Threads", 4)

print("Insert the location for the game's PGN file.")
file = input("> ")
if not os.path.isfile(file):
    os.system('exit')

game, moves = engine.ChessController.read_pgn(file)
analysis = engine.analyse_pgn(file)

#thread = threading.Thread(target=engine.analyse_pgn, args=(game,))
#thread.start()

#while engine.analysed_moves < moves:
    #time.sleep(1)
    #print(engine.analysed_moves)

engine.ChessController.make_command_line_analysis_display(analysis, True)