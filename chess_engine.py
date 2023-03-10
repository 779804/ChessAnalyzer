import chess.pgn
import chess.engine
import chess
import os
from pynput.keyboard import Key, Listener

class ChessController():

    def __init__(self):
        self.currentPos = 0
        pass

    def read_pgn(self, file: str) -> chess.pgn.Game:
        """
        Reads from a PGN file.
        
        Args:
            file (str): File name to read from.

        Returns:
            chess.pgn.Game: Game class of the PGN.
            totalMoves (int): Number of moves the game has.
        """
        if not os.path.isfile(file):
            raise FileNotFoundError("The PGN file to read from does not exist/has not been found.")
        pgn = open(file)
        game = chess.pgn.read_game(pgn)

        totalMoves = 0
        for move in game.mainline_moves():
            totalMoves += 1
        return game, totalMoves
    
    def make_command_line_analysis_display(self, analysis: list, use_unicode_characters=True):
        """
        Creates a command-line display of the game analysis.
        
        Args:
            analysis (list): List containing the analysed game.
            use_unicode_characters (bool): Choose if you would like to use unicode characters for the pieces.
        """
        self.currentPos = 0
        
        def updateDisplay():
            currentPos = self.currentPos
            board = chess.Board()
            board.set_board_fen(analysis[currentPos]["fen"]["board_fen"])
            os.system('cls')
            drawing = str(board)
            if use_unicode_characters == True:
                drawing = drawing.replace('P', '♙')
                drawing = drawing.replace('R', '♜')
                drawing = drawing.replace('N', '♞')
                drawing = drawing.replace('B', '♝')
                drawing = drawing.replace('Q', '♛')
                drawing = drawing.replace('K', '♔')
                drawing = drawing.replace('p', '♟')
                drawing = drawing.replace('r', '♖')
                drawing = drawing.replace('n', '♘')
                drawing = drawing.replace('b', '♗')
                drawing = drawing.replace('q', '♕')
                drawing = drawing.replace('k', '♚')
            evaluation = analysis[currentPos]["eval"]
            str.replace(evaluation, '#', 'M')
            sign = evaluation[:1]
            evaluation = str(int(evaluation[1:len(evaluation)]) / 100)
            evaluation = sign + evaluation

            move = analysis[currentPos]["best_move"]
            if len(move) == 4:
                moveFrom = move[:2]
                moveTo = move[2:4]
                piece = str.upper(str(board.piece_at(getattr(chess, str.upper(moveFrom)))))
                isCapture = analysis[currentPos]["isCapture"]
                bestMove = (piece if piece != 'P' else '') + ('x' if isCapture else '') + moveTo
                if isCapture and piece == "P":
                    bestMove = move[:1] + 'x' + moveTo
            else:
                bestMove = move
            print(drawing)
            print("Evaluation: " + evaluation)
            print("Best move: "+bestMove)

        def on_press(key):
            max = len(analysis)
            if key == Key.right:
                if self.currentPos < max - 1:
                    self.currentPos += 1
                    updateDisplay()
            elif key == Key.left:
                if self.currentPos >= 1:
                    self.currentPos -= 1
                    updateDisplay()

        def on_release(key):
            pass

        updateDisplay()
        
        with Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

class Engine():

    def __init__(self, engine_file: str):
        """
        Creates a new engine class.

        Args:
            engine_file (str): Name of the engine file to use.
        """
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_file)
        self.ChessController = ChessController()
        self.analysed_moves = 0

    def get_engine_configuration(self, config_name="all") -> chess.engine.UciOptionMap | chess.engine.Option:
        """
        Fetches the engine configuration based on the positional arguments.
        Returns false if the configuration is non-existent.

        Args:
            config_name (str): Name of the configuration. Leave blank for the full configuration.

        Returns:
            UciOptionMap | Option: Class containing the engine configuration(s).
        """
        if config_name == "all":
            return self.engine.options
        else:
            options = self.engine.options
            if options[config_name]:
                return options[config_name]
            else:
                return False
            
    def has_configuration(self, config_name: str) -> bool:
        """
        Checks if the engine has the configuration for a specific config name.

        Args:
            config_name (str): Name of the configuration.

        Returns:
            bool: Returns a boolean based on if it exists or not.
        """
        if self.engine.options[config_name]:
            return True
        else:
            return False
            
    def set_engine_configuration(self, config_name: str, config_value) -> bool:
        """
        Sets the engine configuration for the given name and value.

        Args:
            config_name (str): Name of the configuration.
            config_value: Value to change the configuration to.

        Returns:
            bool: Returns a boolean based on if the configuration has succeeded or not.
        """
        
        if not self.engine.options[config_name]:
            return False
        try:
            self.engine.configure({config_name: config_value})
            return True
        except:
            return False

    def analyse_pgn(self, game: chess.pgn.Game | str, depth=12, time=5) -> list:
        """
        Analyses a PGN file and returns the analysis as a list.
        The "analysed_moves" variable shows how many moves have been analysed so far.

        Args:
            game (Game | str): PGN file name or Game class.
            depth (int): Depth of the engine analysis.
            time (int): Time, in seconds, that the engine has to analyse each move.

        Returns:
            list: List containing the analysis of each position.
        """

        self.analysed_moves = 0
        if type(game) == str:
            game, totalMoves = self.ChessController.read_pgn(game)
        analysis = []
        board = game.board()

        moveCount = 0
        for move in game.mainline_moves():
            moveCount +=1
            success = False
            moveTime = time
            while success != True:
                print("Analysing move "+str(moveCount)+", time to analyse: "+str(moveTime))
                info = self.engine.analyse(board, chess.engine.Limit(time=moveTime, depth=depth))
                print(info['score'].white())
                if len(info['pv']) < 2:
                    if str(info['score'].relative)[:1] == "#":
                        board.push(move)

                        if moveCount == totalMoves:
                            score = int(str(info['score'].relative)[1:2])
                            if score < 0:
                                score = "0-1"
                            else:
                                score = "1-0"
                        else:
                            score = str(info['score'].relative)

                        analysis.append({"fen": {"fen": board.fen(), "board_fen": board.board_fen()}, "eval": score, "best_move": "-", "isCapture": board.is_capture(bestMove)})
                        self.analysed_moves += 1
                        return analysis
                    else:
                        moveTime += 1
                        continue
                bestMove = info['pv'][1]
                board.push(move)
                analysis.append({"fen": {"fen": board.fen(), "board_fen": board.board_fen()}, "eval": str(info['score'].relative), "best_move": str(bestMove), "isCapture": board.is_capture(bestMove)})
                self.analysed_moves += 1
                success = True

        return analysis

