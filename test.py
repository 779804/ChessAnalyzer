import os
from chess_engine import *

print("Welcome to the engine analyser.")
print("Insert the file location for the engine you would like to use!")
file = input("> ")
if not os.path.isfile(file):
    os.system('exit')

engine = Engine(file)

print("Insert the location for the game's PGN file.")
file = input("> ")
if not os.path.isfile(file):
    os.system('exit')
analysis = engine.analyse_pgn(file)

engine.ChessController.make_command_line_analysis_display(analysis, True)