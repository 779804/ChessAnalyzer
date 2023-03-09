import chess.pgn
import chess
import os
import time
import threading
from pynput.keyboard import Key, Listener
from stockfish import Stockfish

currentPos = 0
os.system('cls')

print("Insert stockfish version (11 or 15, default = 15):")
stockfishVer = input("> ")
if len(stockfishVer) == 0:
    stockfishVer = "15"
if stockfishVer != "11" or stockfishVer != "15":
    os.system('exit')
stockfishVer = int(stockfishVer)
print("Insert stockfish depth (default = 12):")
stockfishDepth = input("> ")
if stockfishDepth == "":
    stockfishDepth = "12"
try:
    stockfishDepth = int(stockfishDepth)
except ValueError:
    os.system('exit')

def updateDisplay():
    global currentPos
    os.system('cls')
    time.sleep(.1)
    print(positions[currentPos]["drawing"])

    evaluation = positions[currentPos]["eval"]
    if evaluation["type"] == "cp":
        evaluation = evaluation["value"] / 100
        evaluation = str(('+' if evaluation >= 0 else '')) + str(evaluation)
    elif evaluation["type"] == "mate":
        sign = ('+' if evaluation["value"] >=0 else '-')
        evaluation = sign + 'M' + str(abs(evaluation["value"]))


    move = positions[currentPos]["best_move"]
    if len(move) == 4:
        moveFrom = move[:2]
        moveTo = move[2:4]
        board.set_board_fen(positions[currentPos]["fen"]["board_fen"])
        piece = str.upper(str(board.piece_at(getattr(chess, str.upper(moveFrom)))))
        #print(chess.Move(from_square=getattr(chess, str.upper(moveFrom)), to_square=getattr(chess, str.upper(moveTo))))
        isCapture = positions[currentPos]["isCapture"]
        bestMove = (piece if piece != 'P' else '') + ('x' if isCapture else '') + moveTo
        if isCapture and piece == "P":
            bestMove = move[:1] + 'x' + moveTo
    else:
        bestMove = move

    print("Evaluation: " + evaluation)
    print("Best move: "+bestMove)



positions=[]

print("Loading stockfish...")
if stockfishVer == 15:
    stockfish = Stockfish(path="Stockfish 15.1/stockfish-windows-2022-x86-64-avx2", depth=stockfishDepth, parameters={"Threads": 4, "Hash": 4096, "Ponder": True})
elif stockfishVer == 11:
    stockfish = Stockfish(path="Stockfish 11/Windows/stockfish_20011801_x64", depth=stockfishDepth, parameters={"Threads": 4, "Hash": 4096, "Ponder": True})
#positions.append({"fen": {"fen": "ERRORrnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "board_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"}, "eval": 0.0, "best_move": stockfish.get_best_move(), "drawing": stockfish.get_board_visual(), "isCapture": False})

pgn = open("Game.pgn")
game = chess.pgn.read_game(pgn)

board = game.board()

max = 0
for move in game.mainline_moves():
    max += 1

count = 1
for move in game.mainline_moves():
    print("Analyzing move "+str(count)+"/"+str(max)+".")

    stockfish.set_fen_position(board.fen())
    bestMove = stockfish.get_best_move()
    positions.append({"fen": {"fen": board.fen(), "board_fen": board.board_fen()}, "eval": stockfish.get_evaluation(), "best_move": bestMove, "drawing": stockfish.get_board_visual(), "isCapture": stockfish.will_move_be_a_capture(bestMove) != stockfish.Capture.NO_CAPTURE})
    board.push(move)
    
    count+=1

updateDisplay()

def on_press(key):
    global currentPos
    if key == Key.right:
        if currentPos < max - 1:
            currentPos += 1
            updateDisplay()
    elif key == Key.left:
        if currentPos >= 1:
            currentPos -= 1
            updateDisplay()


def on_release(key):
    pass

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()