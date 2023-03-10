import chess.pgn
import chess.engine
import chess
import os
import time
import threading
from pynput.keyboard import Key, Listener

print("Insert leela depth (default = 18):")
engineDepth = input("> ")
if engineDepth == "":
    engineDepth = "18"
try:
    engineDepth = int(engineDepth)
except ValueError:
    os.system('exit')


currentPos = 0
os.system('cls')

def updateDisplay():
    global currentPos
    os.system('cls')
    drawing = str(positions[currentPos]["drawing"])
   # drawing = drawing.replace('P', '♙')
   # drawing = drawing.replace('R', '♜')
   # drawing = drawing.replace('N', '♞')
   # drawing = drawing.replace('B', '♝')
   # drawing = drawing.replace('Q', '♛')
   # drawing = drawing.replace('K', '♔')
   # drawing = drawing.replace('p', '♟')
   # drawing = drawing.replace('r', '♖')
   # drawing = drawing.replace('n', '♘')
   # drawing = drawing.replace('b', '♗')
   # drawing = drawing.replace('q', '♕')
   # drawing = drawing.replace('k', '♚')
    evaluation = positions[currentPos]["eval"]
    str.replace(evaluation, '#', 'M')
    sign = evaluation[:1]
    evaluation = str(int(evaluation[1:len(evaluation)]) / 100)
    evaluation = sign + evaluation

    move = positions[currentPos]["best_move"]
    if len(move) == 4:
        moveFrom = move[:2]
        moveTo = move[2:4]
        board.set_board_fen(positions[currentPos]["fen"]["board_fen"])
        piece = str.upper(str(board.piece_at(getattr(chess, str.upper(moveFrom)))))
        isCapture = positions[currentPos]["isCapture"]
        bestMove = (piece if piece != 'P' else '') + ('x' if isCapture else '') + moveTo
        if isCapture and piece == "P":
            bestMove = move[:1] + 'x' + moveTo
    else:
        bestMove = move
    print(drawing)
    print("Evaluation: " + evaluation)
    print("Best move: "+bestMove)


positions=[]

print("Loading Leela...")

engine = chess.engine.SimpleEngine.popen_uci(os.path.abspath("EngineLeela\\lc0"))

os.system('cls')



pgn = open("GameSmall.pgn")
game = chess.pgn.read_game(pgn)

board = game.board()
#print(board)
max = 0
for move in game.mainline_moves():
    max += 1

count = 1
for move in game.mainline_moves():
    print("Analyzing move "+str(count)+"/"+str(max)+".")
    info = engine.analyse(board, chess.engine.Limit(time=5, depth=engineDepth))
    bestMove = info['pv'][1]
    board.push(move)
    positions.append({"fen": {"fen": board.fen(), "board_fen": board.board_fen()}, "eval": str(info['score'].relative), "best_move": str(bestMove), "drawing": board, "isCapture": board.is_capture(bestMove)})
    
    
    
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
if __name__ == "__main__":
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()