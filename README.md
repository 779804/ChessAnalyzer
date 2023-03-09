# ChessEngine
A project I am currently working on that utilizes python to control engines such as Stockfish and Leela, and provide full game analysis with a GUI included.
You are free to fork, modify, or utilize this project for yourself if you would like to.

# Engine compatibility
This project is compatible with all engines that utilize the [Universal Chess Interface](https://backscattering.de/chess/uci/) protocol.

# Instructions
* Launch the main file for the program.
* Once the interface has opened, select the engine you would like to use (see compatible engines above).
* Configure the settings for the engine. Not all engines will have the examples below. The primary details you want to focus on are:
   - Threads: set the number of threads to the maximum available, though you can leave 1 or 2 threads for other tasks.
   - Hash: set the hast to (nearly) the maximum amount of RAM (memory) available. The value is specified in MB (Mega-bytes) and should, in most cases, be written in powers of 2. Examples:
      - 1024 = 1 GB of RAM.
      - 2048 = 2 GB of RAM.
      - 4096 = 4 GB of RAM.
      - 8192 = 8 GB of RAM.
   - Depth: the depth of an engine is how many moves it will predict, therefore enhancing the analysis of the engine. The default for this is 12. Reminder: the larger the value, the slower the analysis might be.
* You may now paste in the PGN for your game and it will be analysed utilizing your computer's hardware.
* Once the analysis is concluded, you can scroll through the moves using the GUI on the right or the right and left arrow keys on your keyboard.

# Credits
I am responsible for coding the engine analysis and connection between the program and the User Interface.
The chess board display has been mostly copied from AlejoG10's [python-chess-ai-yt](https://github.com/AlejoG10/python-chess-ai-yt) project.

# Terms of use
This program is free to use and distributed under the [MIT License](https://github.com/779804/ChessAnalyzer/blob/main/LICENSE). Distribution, commercial use, modification and private use are all authorized. The copyright notice and permission notice must be included in all copies or substantial portions of the Software.
