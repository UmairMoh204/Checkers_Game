"""
Team Checked Out
Team members: Nicholas Lobaugh, Umair Mohammed, Kai Yamanishi
This program implements a simple game of checkers. It has three main sections. THe first imports all the graphics. The
second is the Board class, which implements the GUI, and holds all the data related to the game. The third is a
collection of functions that operate on the data within the Board class. Testing was carried out by manually working
through every edge case we could think of at each stage of the program's development.
"""

# Import statements. tkinter for the gui, imageTools for bringing in graphics, and functools to create callback
# functions.
from tkinter import *
from imageTools import *
from functools import partial

# set up checker piece images
bigRKingOpen = Image.open("red king piece (logo).png")
bigRKing = ImageTk.PhotoImage(bigRKingOpen)

BKingOpen = Image.open("black king piece (small, gold).png")
bKing = ImageTk.PhotoImage(BKingOpen)

RKingOpen = Image.open("red king piece (small, gold).png")
rKing = ImageTk.PhotoImage(RKingOpen)

bPieceOpen = Image.open("black piece (small).png")
bPiece = ImageTk.PhotoImage(bPieceOpen)

rPieceOpen = Image.open("red piece (small).png")
rPiece = ImageTk.PhotoImage(rPieceOpen)

GreyOpen = Image.open("transparent.png")
Grey = ImageTk.PhotoImage(GreyOpen)


class Board():
    """
    This class implements a GUI and set of dictionaries that represent a checkers board. It interacts heavily with a
    series of functions kept below it that modify the data it holds, and the state of the GUI.
    """
    def __init__(self):
        # Create the gameData dictionary, which holds all data that the outside functions need to access which is not
        # directly related to the board. A few more elements are added to this dictionary later in this function.
        gameData = {}
        gameData["currentPlayer"] = "r"  # Stores the letter of the current player.
        gameData["Bpoints"] = 0  # Stores the number of red pieces black has captured.
        gameData["Rpoints"] = 0  # Stores the number of black pieces red has captured.
        gameData["MadeMove"] = False  # Flag used by endTurn to determine whether a move has been made.

        # Create and seed the board dictionary
        boardState = self.seedBoard()

        # set up the overall window, as an instance variable
        self.mainWin = Toplevel(root)
        self.mainWin.title("Checkers!")
        self.mainWin.state('zoomed')

        # Set up the board frame and buttons
        self.boardFrame = tk.Frame(self.mainWin, bg="white")
        self.boardFrame.grid(row=2, column=1)

        # set up a frame for labels and buttons to the right of the board
        self.tallyFrame = tk.Frame(self.mainWin, pady=10)
        self.tallyFrame.grid(row=2, column=2)

        emptyLabel1 = tk.Label(self.tallyFrame, text="")
        emptyLabel1.grid(row=1, column=0, pady=70)

        emptyLabel2 = tk.Label(self.tallyFrame, text="")
        emptyLabel2.grid(row=4, column=0, pady=55)

        buttonBoardState = self.buttonBoard(gameData, boardState)

        # Adds a quit button
        QuitButton = tk.Button(self.tallyFrame, padx=10, pady=5, font="Arial 10", bg="white")
        QuitButton["text"] = "Quit"
        QuitButton["command"] = self.quit
        QuitButton.grid(row=5, column=0)

        # Adds a restart button
        RestartButton = tk.Button(self.tallyFrame, padx=10, pady=5, font="Arial 10", bg="white")
        RestartButton["text"] = "Restart"
        RestartButton["command"] = self.restart
        RestartButton.grid(row=6, column=0, pady=5)

        # Adds label that displays whose turn it is
        playerTurnLabel = tk.Label(self.mainWin, text="Red's Turn", foreground="red", font="Arial 15 bold")
        gameData["playerTurn"] = playerTurnLabel
        playerTurnLabel.grid(row=1, column=1)

        # Displaying point tallies
        BlackPoints = tk.Label(self.tallyFrame, font="Arial 12")
        gameData["BlackScoreBoard"] = BlackPoints
        BlackPoints["text"] = ("Black Score: " + str(gameData["Bpoints"]))
        BlackPoints.grid(row=2, column=0, pady=20)

        RedPoints = tk.Label(self.tallyFrame, font="Arial 12")
        gameData["RedScoreBoard"] = RedPoints
        RedPoints["text"] = ("Red Score: " + str(gameData["Rpoints"]))
        RedPoints["foreground"] = "red"
        RedPoints.grid(row=3, column=0, pady=20)

        # Adds "End Turn" button, mainly just to cancel chain jumps after moving at least once
        EndTurn = tk.Button(self.tallyFrame, padx=5, pady=3, font="Arial 10", bg="white")
        EndTurn["text"] = "End Turn"
        gameData["playerEndTurn"] = EndTurn
        EndTurn.grid(row=0, column=0)
        EndTurn["command"] = partial(endTurn, gameData, boardState, buttonBoardState)

        # Adds labels with instructions to the left of the board
        instructionsFrame = tk.Frame(self.mainWin)
        instructionsFrame.grid(row=2, column=0)

        instructionTitleLabel = tk.Label(instructionsFrame, font="Times 15 italic")
        instructionTitleLabel["text"] = "Instructions"
        instructionTitleLabel.grid(row=0, column=0)

        instructionLabel = tk.Label(instructionsFrame, font="Times 10")
        instructionLabel["text"] = "\n" \
                                   "- Red goes first. \n" \
                                   "\n" \
                                   "- When it is your turn, click on one \n" \
                                   "  of your pieces to check which moves \n" \
                                   "  you can make with that piece. \n" \
                                   "\n" \
                                   "- The game will highlight available \n" \
                                   "  moves in yellow and available jumps \n" \
                                   "  in orange. Click on yellow spaces to \n" \
                                   "  move your piece once, or orange to \n" \
                                   "  jump over an enemy piece and take it. \n" \
                                   "  Multiple jumps can be made in one turn. \n" \
                                   "\n" \
                                   "- If you wish to end your turn between \n" \
                                   "  jumps, click the 'end Turn' button. \n" \
                                   "\n" \
                                   "- If a piece makes it to the other end \n" \
                                   "  of the board, it becomes a king and \n" \
                                   "  can move in any direction. \n" \
                                   "\n" \
                                   "- The first player to capture all 12 \n" \
                                   "  of the other player's pieces wins!" \
                                   "\n" \
                                   "\n" \
                                   "\n" \
                                   "         Thank you for playing! \n" \
                                   "\n" \
                                   "             Made by: \n" \
                                   "\n" \
                                   "          Kai Yamanishi \n" \
                                   "          Umair Mohammed \n" \
                                   "         Nicholas Lobaugh"
        instructionLabel.grid(row=1, column=0)


        # Adds a frame that contains a label that is updated with win screen information when one player wins,
        # as well as two buttons: one to start a new game, and the other to quit the program.
        winFrame = tk.Frame(self.mainWin, bg="white")
        gameData["playerWin"] = winFrame
        winFrame["relief"] = tk.RAISED
        winFrame["bd"] = 4

        winLabel = tk.Label(winFrame, padx=15, pady=10, bg="white")
        winLabel["font"] = "Times 50 bold italic"
        gameData["playerWinText"] = winLabel
        winLabel.grid(row=0, column=0)

        winButtonFrame = tk.Frame(winFrame, bg="white")
        winButtonFrame.grid(row=1, column=0)

        playAgainButton = tk.Button(winButtonFrame, padx=10, pady=5, bg="white")
        playAgainButton["text"] = "Play again?"
        playAgainButton["font"] = "Arial 10 bold"
        playAgainButton["command"] = self.restart
        playAgainButton.grid(row=0, column=0, padx=20, pady=15)

        winQuitButton = tk.Button(winButtonFrame, padx=10, pady=5, bg="white")
        winQuitButton["text"] = "Quit"
        winQuitButton["font"] = "Arial 10 bold"
        winQuitButton["command"] = self.quit
        winQuitButton.grid(row=0, column=1, padx=20, pady=15)

        # Title label
        titleLabel = tk.Label(self.mainWin)
        titleLabel["text"] = "Checkers!"
        titleLabel["font"] = "times 40 bold"
        titleLabel.grid(row=0, column=1)

        # adds red king image to right of game
        imageLabel = tk.Label(self.mainWin)
        imageLabel["image"] = bigRKing
        imageLabel.grid(row=2, column=3, padx=60)

    def seedBoard(self):
        """
        Creates and returns a dictionary containing a checkers board set up for a new game. Each entry in the
        dictionary corresponds to a square on the board, and are numbered as follows: 12, 14, 16, 18, 22, 24, ... 86, 88
        Each entry holds one of three values, "r", "e", or "b", which represent a red piece, an empty square, and a
        black piece respectively. checkKing can capitalise "r"'s and "b"'s, which represent the piece becoming a king.
        """
        squareNum = 12
        boardState = {}
        while squareNum <= 88:
            if squareNum <= 38:
                boardState[squareNum] = "r"
            elif squareNum <= 58:
                boardState[squareNum] = "e"
            else:
                boardState[squareNum] = "b"

            if squareNum % 10 != 8:
                squareNum = squareNum + 2
            else:
                squareNum = squareNum + 4
        print(boardState)
        return boardState

    def buttonBoard(self, gameData, boardState):
        """
        Creates and returns the dictionary of buttons that make up the board. Each entry corresponds to a space on the
        board in the same way as the entries in boardState, and share the same numbering scheme. Rather than characters
        though, these entries contain the tkinter buttons that make up the interactive part of the board.
        :param gameData: Dictionary with all non piece related data.
        :param boardState: Main board state dictionary.
        :return:
        """
        buttonBoardState = {}
        squareNum = 12
        for row in range(8, 0, -1):
            for column in range(8, 0, -1):
                if column % 2 == 1 and row % 2 == 0:    # sets up buttons on even rows
                    if squareNum <= 38:
                        boardButton = tk.Button(self.boardFrame, image=rPiece, height=60, width=60, bg="grey", relief=tk.FLAT,
                                                command=partial(checkMove, squareNum, gameData, boardState, buttonBoardState))
                        boardButton.grid(row=row, column=column)
                    elif squareNum <= 58:
                        boardButton = tk.Button(self.boardFrame, image=Grey, height=60, width=60, relief=tk.FLAT, bg='grey',
                                                command=partial(checkMove, squareNum, gameData, boardState, buttonBoardState))
                        boardButton.grid(row=row, column=column)
                    else:
                        boardButton = tk.Button(self.boardFrame, image=bPiece, height=60, width=60, foreground="white", bg='grey', relief=tk.FLAT,
                                                command=partial(checkMove, squareNum, gameData, boardState, buttonBoardState))
                        boardButton.grid(row=row, column=column)

                    buttonBoardState[squareNum] = boardButton

                    if squareNum % 10 != 8:
                        squareNum = squareNum + 2
                    else:
                        squareNum = squareNum + 4
                elif column % 2 == 0 and row % 2 == 1:  # sets up buttons on odd rows
                    if squareNum <= 38:
                        boardButton = tk.Button(self.boardFrame, image=rPiece, height=60, width=60, bg="grey", relief=tk.FLAT,
                                                command=partial(checkMove, squareNum, gameData, boardState, buttonBoardState))
                        boardButton.grid(row=row, column=column)
                    elif squareNum <= 58:
                        boardButton = tk.Button(self.boardFrame, image=Grey, height=60, width=60, relief=tk.FLAT, bg="grey",
                                                command=partial(checkMove, squareNum, gameData, boardState, buttonBoardState))
                        boardButton.grid(row=row, column=column)
                    else:
                        boardButton = tk.Button(self.boardFrame, image=bPiece, height=60, width=60, foreground="white", bg="grey", relief=tk.FLAT,
                                                command=partial(checkMove, squareNum, gameData, boardState, buttonBoardState))
                        boardButton.grid(row=row, column=column)

                    buttonBoardState[squareNum] = boardButton

                    if squareNum % 10 != 8:
                        squareNum = squareNum + 2
                    else:
                        squareNum = squareNum + 4
        return buttonBoardState

    def run(self):
        """This takes no inputs, and sets the GUI running"""
        self.mainWin.mainloop()

    def quit(self):
        """This is a callback method attached to the two quit buttons.
        It destroys the main window, which ends the program"""
        self.mainWin.destroy()
        sys.exit()

    def restart(self):
        """Destroys the current game, and creates a new checkers game"""
        self.mainWin.destroy()
        myBoard = Board()
        myBoard.run()


"""
The following functions all interact with the Board class in some way. They are organised roughly by the order in which 
they are called, and their complexity. There is also safelower, which we don't talk about.
"""

def safelower(hopefullyAString):
    """
    This function is a wrapper for the standard lower() function, that prevents it from taking in input that would
    throw an error. This was done to prevent the program from throwing nonfatal errors when checkMove is called for a
    piece on an edge of the board, as this edge case results in a noneType being passed to checkMove and checkJump, and
    thus through lower(). the alternative was hours of refactoring.
    """
    if type(hopefullyAString) == str:
        return hopefullyAString.lower()

def checkMove(squareNum, gameData, boardState, buttonBoardState):
    '''
    Highlights all the available moves from a clicked on piece by changing tile colors, and also switching their on
    click function to makeMove, so when the player clicks on one of those moves, it calls makeMove. Also calls
    checkJump, which does a similar thing, but for jumps.
    :param squareNum: Dictionary key of the square that has been clicked on.
    :param gameData: Dictionary with all non piece related data.
    :param boardState: Main board state dictionary.
    :param buttonBoardState: Dictionary of buttons for the board squares.
    :return:
    '''
    # Clean up any previously highlighted moves.
    for key in boardState:
        if boardState[key] == "e":
            buttonBoardState[key]["image"] = Grey
            buttonBoardState[key]["bg"] = "grey"
            buttonBoardState[key]["command"] = partial(checkMove, squareNum, gameData, boardState, buttonBoardState)

    # Checks for moves
    if gameData["currentPlayer"] == "b" or gameData["currentPlayer"] == "r" and boardState[squareNum] == "R":  # When black is the current player
        if boardState[squareNum].lower() == gameData["currentPlayer"]:  # If the piece clicked on is the current player's colour
            if (squareNum // 10) % 2 == 0:  # If the piece is on an even row
                # These next two sets of if statements check the state of the two spaces in front of the piece that was clicked on
                if boardState.get(squareNum - 12) == "e":  # If the space is empty, highlight it and change it's callback function to makeMove
                    buttonBoardState[squareNum - 12]["bg"] = "yellow"
                    buttonBoardState[squareNum - 12]["command"] = partial(makeMove, squareNum - 12, squareNum, gameData,
                                                                          boardState, buttonBoardState)
                # This is the same as the previous section, but for the other square in front of the selected piece.
                if boardState.get(squareNum - 10) == "e":
                    buttonBoardState[squareNum - 10]["bg"] = "yellow"
                    buttonBoardState[squareNum - 10]["command"] = partial(makeMove, squareNum - 10, squareNum, gameData,
                                                                          boardState, buttonBoardState)
            # This is the same as the previous section, but for pieces on an odd row.
            elif (squareNum // 10) % 2 == 1:
                if boardState.get(squareNum - 8) == "e":
                    buttonBoardState[squareNum - 8]["bg"] = "yellow"
                    buttonBoardState[squareNum - 8]["command"] = partial(makeMove, squareNum - 8, squareNum, gameData,
                                                                          boardState, buttonBoardState)

                if boardState.get(squareNum - 10) == "e":
                    buttonBoardState[squareNum - 10]["bg"] = "yellow"
                    buttonBoardState[squareNum - 10]["command"] = partial(makeMove, squareNum - 10, squareNum, gameData,
                                                                          boardState, buttonBoardState)
    # This is the same as the previous section, but for when the gameData is Red.
    if gameData["currentPlayer"] == "r" or gameData["currentPlayer"] == "b" and boardState[squareNum] == "B":
        if boardState[squareNum].lower() == gameData["currentPlayer"]:
            if (squareNum // 10) % 2 == 1:
                if boardState.get(squareNum + 12) == "e":
                    buttonBoardState[squareNum + 12]["bg"] = "yellow"
                    buttonBoardState[squareNum + 12]["command"] = partial(makeMove, squareNum + 12, squareNum, gameData,
                                                                          boardState, buttonBoardState)

                if boardState.get(squareNum + 10) == "e":
                    buttonBoardState[squareNum + 10]["bg"] = "yellow"
                    buttonBoardState[squareNum + 10]["command"] = partial(makeMove, squareNum + 10, squareNum, gameData,
                                                                          boardState, buttonBoardState)

            elif (squareNum // 10) % 2 == 0:
                if boardState.get(squareNum + 8) == "e":
                    buttonBoardState[squareNum + 8]["bg"] = "yellow"
                    buttonBoardState[squareNum + 8]["command"] = partial(makeMove, squareNum + 8, squareNum, gameData,
                                                                          boardState, buttonBoardState)

                if boardState.get(squareNum + 10) == "e":
                    buttonBoardState[squareNum + 10]["bg"] = "yellow"
                    buttonBoardState[squareNum + 10]["command"] = partial(makeMove, squareNum + 10, squareNum, gameData,
                                                                          boardState, buttonBoardState)
    # Call checkJump, a function that checks for possible jumps.
    checkJump(squareNum, gameData, boardState, buttonBoardState)


def makeMove(newSquareNum, oldSquareNum, gameData, boardState, buttonBoardState):
    """
    Updates boardState and buttonBoardState to reflect the move of a piece, and cleans up highlighting from
    checkJump and checkMove.
    :param newSquareNum: Dictionary key of the square the piece is moving too.
    :param oldSquareNum: Dictionary key of the square the piece is coming from.
    :param gameData: Dictionary with all non piece related data.
    :param boardState: Main board state dictionary.
    :param buttonBoardState: Dictionary of buttons for the board squares.
    :return:
    """
    # Update the boardState dictionary with new values.
    boardState[newSquareNum] = boardState[oldSquareNum]
    boardState[oldSquareNum] = "e"

    # Update the buttonBoard buttons with new colours and commands.
    buttonBoardState[newSquareNum]["image"] = buttonBoardState[oldSquareNum]["image"]
    buttonBoardState[newSquareNum]["bg"] = buttonBoardState[oldSquareNum]["bg"]
    buttonBoardState[newSquareNum]["text"] = buttonBoardState[oldSquareNum]["text"]
    buttonBoardState[newSquareNum]["relief"] = buttonBoardState[oldSquareNum]["relief"]
    buttonBoardState[newSquareNum]["foreground"] = buttonBoardState[oldSquareNum]["foreground"]
    buttonBoardState[newSquareNum]["command"] = partial(checkMove, newSquareNum, gameData, boardState, buttonBoardState)

    buttonBoardState[oldSquareNum]["image"] = Grey
    buttonBoardState[oldSquareNum]["bg"] = "grey"
    buttonBoardState[oldSquareNum]["text"] = ""
    buttonBoardState[oldSquareNum]["relief"] = tk.FLAT
    buttonBoardState[oldSquareNum]["command"] = partial(checkMove, oldSquareNum, gameData, boardState, buttonBoardState)

    # Clean up extra highlighted moves that were not made.
    cleanHighlights(gameData, boardState, buttonBoardState)

    # Trigger the MadeMove flag, which is used in endTurn
    gameData["MadeMove"] = True

    # Promote the piece to a king if it has reached the opposite end of the board.
    checkKing(newSquareNum, boardState, buttonBoardState)

    # Pass the turn to the other player.
    endTurn(gameData, boardState, buttonBoardState)


def checkJump(squareNum, gameData, boardState, buttonBoardState):
    """
    Similar to checkMove, but instead checks for instances where a piece can jump over and take an enemy piece. It
    highlights these jumps, and changes those highlighted square's callback function to makeJump. Finally, it returns a
    flag, availableJumps, which is true if there is at least one jump available to a piece, and false is none are.
    This is used in makeJump to determine whether to end the turn, or wait for the player to either continue jumping,
    or press the end turn button.
    :param squareNum: Dictionary key of the square that has been clicked on.
    :param gameData: Dictionary with all non piece related data.
    :param boardState: Main board state dictionary.
    :param buttonBoardState: Dictionary of buttons for the board squares.
    :return:
    """
    availableJump = False
    # Checks for jumps
    if gameData["currentPlayer"] == "b" or gameData["currentPlayer"] == "r" and boardState[squareNum] == "R":  # When black is the current player or piece is red king
        if boardState[squareNum].lower() == gameData["currentPlayer"]:  # If the piece clicked on is the current player's colour
            if (squareNum // 10) % 2 == 0:  # If the piece is on an even row
                # These next two sets of if statements check the state of the two spaces in front of the piece that was clicked on
                if safelower(boardState.get(squareNum - 12)) == "r" and boardState[squareNum].lower() == "b" or safelower(boardState.get(squareNum - 12)) == "b" and boardState[squareNum] == "R":  # If the space is the opposite color, check the square on the far side of it
                    if boardState.get(squareNum - 22) == "e":  # If that square is empty, highlight it orange, and change its callback function to makeJump()
                        buttonBoardState[squareNum - 22]["bg"] = "orange"
                        buttonBoardState[squareNum - 22]["command"] = partial(makeJump, squareNum - 22, squareNum, squareNum - 12,
                                                                            gameData,
                                                                            boardState, buttonBoardState)
                        buttonBoardState[squareNum - 22]["state"] = "normal"
                        availableJump = True  # Switch availableJump to True.
                # This is the same as the previous section, but for the other square in front of the selected piece.
                if safelower(boardState.get(squareNum - 10)) == "r" and boardState[squareNum].lower() == "b" or safelower(boardState.get(squareNum - 10)) == "b" and boardState[squareNum] == "R":
                    if boardState.get(squareNum - 18) == "e":
                        buttonBoardState[squareNum - 18]["bg"] = "orange"
                        buttonBoardState[squareNum - 18]["command"] = partial(makeJump, squareNum - 18, squareNum,
                                                                              squareNum - 10,
                                                                              gameData,
                                                                              boardState, buttonBoardState)
                        buttonBoardState[squareNum - 18]["state"] = "normal"
                        availableJump = True
            # This is the same as the previous section, but for pieces on an odd row.
            elif (squareNum // 10) % 2 == 1:
                if safelower(boardState.get(squareNum - 8)) == "r" and boardState[squareNum].lower() == "b" or safelower(boardState.get(squareNum - 8)) == "b" and boardState[squareNum] == "R":
                    if boardState.get(squareNum - 18) == "e":
                        buttonBoardState[squareNum - 18]["bg"] = "orange"
                        buttonBoardState[squareNum - 18]["command"] = partial(makeJump, squareNum - 18, squareNum,
                                                                              squareNum - 8,
                                                                              gameData,
                                                                              boardState, buttonBoardState)
                        buttonBoardState[squareNum - 18]["state"] = "normal"
                        availableJump = True

                if safelower(boardState.get(squareNum - 10)) == "r" and boardState[squareNum].lower() == "b" or safelower(boardState.get(squareNum - 10)) == "b" and boardState[squareNum] == "R":
                    if boardState.get(squareNum - 22) == "e":
                        buttonBoardState[squareNum - 22]["bg"] = "orange"
                        buttonBoardState[squareNum - 22]["command"] = partial(makeJump, squareNum - 22, squareNum,
                                                                              squareNum - 10,
                                                                              gameData,
                                                                              boardState, buttonBoardState)
                        buttonBoardState[squareNum - 22]["state"] = "normal"
                        availableJump = True
    # This is the same as the previous section, but for when the gameData is Red or piece is black king.
    if gameData["currentPlayer"] == "r" or gameData["currentPlayer"] == "b" and boardState[squareNum] == "B":
        if boardState[squareNum].lower() == gameData["currentPlayer"]:  # If the piece clicked on is the current player's colour
            if (squareNum // 10) % 2 == 0:  # If the piece is on an even row
                # These next two sets of if statements check the state of the two spaces in front of the piece that was clicked on
                if safelower(boardState.get(squareNum + 10)) == "b" and boardState[squareNum].lower() == "r" or safelower(boardState.get(squareNum + 10)) == "r" and boardState[squareNum] == "B":  # If the space is the opposite color, check the square on the far side of it
                    if boardState.get(squareNum + 22) == "e":  # If that square is empty, highlight it orange, and change its callback function to makeJump()
                        buttonBoardState[squareNum + 22]["bg"] = "orange"
                        buttonBoardState[squareNum + 22]["command"] = partial(makeJump, squareNum + 22, squareNum,
                                                                              squareNum + 10,
                                                                              gameData,
                                                                              boardState, buttonBoardState)
                        buttonBoardState[squareNum + 22]["state"] = "normal"
                        availableJump = True
                # This is the same as the previous section, but for the other square in front of the selected piece.
                if safelower(boardState.get(squareNum + 8)) == "b" and boardState[squareNum].lower() == "r" or safelower(boardState.get(squareNum + 8)) == "r" and boardState[squareNum] == "B":
                    if boardState.get(squareNum + 18) == "e":
                        buttonBoardState[squareNum + 18]["bg"] = "orange"
                        buttonBoardState[squareNum + 18]["command"] = partial(makeJump, squareNum + 18, squareNum,
                                                                              squareNum + 8,
                                                                              gameData,
                                                                              boardState, buttonBoardState)
                        buttonBoardState[squareNum + 18]["state"] = "normal"
                        availableJump = True
            # This is the same as the previous section, but for pieces on an odd row.
            elif (squareNum // 10) % 2 == 1:
                if safelower(boardState.get(squareNum + 10)) == "b" and boardState[squareNum].lower() == "r" or safelower(boardState.get(squareNum + 10)) == "r" and boardState[squareNum] == "B":
                    if boardState.get(squareNum + 18) == "e":
                        buttonBoardState[squareNum + 18]["bg"] = "orange"
                        buttonBoardState[squareNum + 18]["command"] = partial(makeJump, squareNum + 18, squareNum,
                                                                              squareNum + 10,
                                                                              gameData,
                                                                              boardState, buttonBoardState)
                        buttonBoardState[squareNum + 18]["state"] = "normal"
                        availableJump = True

                if safelower(boardState.get(squareNum + 12)) == "b" and boardState[squareNum].lower() == "r" or safelower(boardState.get(squareNum + 12)) == "r" and boardState[squareNum] == "B":
                    if boardState.get(squareNum + 22) == "e":
                        buttonBoardState[squareNum + 22]["bg"] = "orange"
                        buttonBoardState[squareNum + 22]["command"] = partial(makeJump, squareNum + 22, squareNum,
                                                                              squareNum + 12,
                                                                              gameData,
                                                                              boardState, buttonBoardState)
                        buttonBoardState[squareNum + 22]["state"] = "normal"
                        availableJump = True
    return availableJump


def makeJump(newSquareNum, oldSquareNum, jumpedSquare, gameData, boardState, buttonBoardState):
    """
    Updates boardState and buttonBoardState to reflect the move of a piece. Cleans up highlighting from checkJump and
    checkMove Afterwards, calls checkJump to see if there are further possible jumps for the jumped piece. If so, it
    disables all board interaction other than making those jumps. If there are no available jumps left, it simply ends
    the turn.
    :param newSquareNum: Dictionary key of the square the piece is moving too.
    :param oldSquareNum: Dictionary key of the square the piece is coming from.
    :param jumpedSquare: Dictionary key of the square with the piece that has been jumped.
    :param gameData: Dictionary with all non piece related data.
    :param boardState: Main board state dictionary.
    :param buttonBoardState: Dictionary of buttons for the board squares.
    :return:
    """
    # Update the boardState dictionary with new values.
    boardState[newSquareNum] = boardState[oldSquareNum]
    boardState[oldSquareNum] = "e"
    boardState[jumpedSquare] = "e"

    # Update the buttonBoard buttons with new images and commands, depending on the gameData color.
    buttonBoardState[newSquareNum]["image"] = buttonBoardState[oldSquareNum]["image"]
    buttonBoardState[newSquareNum]["bg"] = buttonBoardState[oldSquareNum]["bg"]
    buttonBoardState[newSquareNum]["text"] = buttonBoardState[oldSquareNum]["text"]
    buttonBoardState[newSquareNum]["relief"] = buttonBoardState[oldSquareNum]["relief"]
    buttonBoardState[newSquareNum]["foreground"] = buttonBoardState[oldSquareNum]["foreground"]
    buttonBoardState[newSquareNum]["command"] = partial(checkMove, newSquareNum, gameData, boardState,
                                                        buttonBoardState)
    buttonBoardState[oldSquareNum]["image"] = Grey
    buttonBoardState[oldSquareNum]["bg"] = "grey"
    buttonBoardState[oldSquareNum]["text"] = ""
    buttonBoardState[oldSquareNum]["relief"] = tk.FLAT
    buttonBoardState[oldSquareNum]["command"] = partial(checkMove, oldSquareNum, gameData, boardState,
                                                        buttonBoardState)
    buttonBoardState[jumpedSquare]["image"] = Grey
    buttonBoardState[jumpedSquare]["bg"] = "grey"
    buttonBoardState[jumpedSquare]["text"] = ""
    buttonBoardState[jumpedSquare]["relief"] = tk.FLAT
    buttonBoardState[jumpedSquare]["command"] = partial(checkMove, jumpedSquare, gameData, boardState,
                                                        buttonBoardState)

    # Increment the score of the current player.
    incrementScore(gameData)

    # Promote the piece to a king if it has reached the opposite end of the board.
    checkKing(newSquareNum, boardState, buttonBoardState)

    # Clean up extra highlighted moves that were not made.
    cleanHighlights(gameData, boardState, buttonBoardState)

    # Update MadeMove to true, and highlight the endturn button to remind the player that using it is now an option.
    gameData["MadeMove"] = True
    gameData["playerEndTurn"]["bg"] = "orange"

    # disables all buttons so the player can't move infinitely
    for key in boardState:
        buttonBoardState[key]["state"] = "disabled"

    # Call checkMove, and store whether it found any jumps
    availableJump = checkJump(newSquareNum, gameData, boardState, buttonBoardState)

    # If no jumps found, endTurn()
    if not availableJump:
        endTurn(gameData, boardState, buttonBoardState)
        return


def checkKing(squareNum, BoardState, buttonBoardState):
    """
    Checks if a piece has reached the opposite side of the board it started on, and updates its value in board state
    to a capital letter if so, to indicate it has become a king.
    :param squareNum: Dictionary key of the square that has been clicked on.
    :param BoardState: Main board state dictionary.
    :param buttonBoardState: Dictionary of buttons for the board squares.
    :return:
    """
    if BoardState[squareNum] == "r" and squareNum >= 82:
        BoardState[squareNum] = "R"
        buttonBoardState[squareNum]["image"] = rKing
    if BoardState[squareNum] == "b" and squareNum <= 18:
        BoardState[squareNum] = "B"
        buttonBoardState[squareNum]["image"] = bKing


def endTurn(gameData, boardState, buttonBoardState):
    """
    Updates gameData["currentPlayer"] to the other color.
    :param gameData: Dictionary with all none piece related data.
    :param boardState: Main board state dictionary.
    :param buttonBoardState: Dictionary of buttons for the board squares.
    :return:
    """
    # If no move has been made, return.
    if not gameData["MadeMove"]:
        return

    # Clean up extra highlighted moves that were not made, so long as a move or jump has been made.
    cleanHighlights(gameData, boardState, buttonBoardState)

    # Re-enable all buttons which might have been disabled by makeJump
    for key in boardState:
        buttonBoardState[key]["state"] = "normal"

    # Update the label that displays the current players turn.
    if gameData["currentPlayer"] == "r":
        gameData["currentPlayer"] = "b"
        gameData["playerTurn"]["text"] = "Black's Turn"
        gameData["playerTurn"]["foreground"] = "black"
    else:
        gameData["currentPlayer"] = "r"
        gameData["playerTurn"]["text"] = "Red's Turn"
        gameData["playerTurn"]["foreground"] = "red"

    # Flip MadeMove back to false
    gameData["MadeMove"] = False
    gameData["playerEndTurn"]["bg"] = "white"

    # Check if one player or the other has won, and display the winscreen if so.
    checkWin(gameData, boardState, buttonBoardState)


def checkWin(gameData, boardState, buttonBoardState):
    """
    Checks if one player has taken all enemy pieces. If so, it updates and reveals the win screen frame and label, and
    disables the board buttons.
    :param gameData: Dictionary with all non piece related data.
    :param boardState: Main board state dictionary.
    :param buttonBoardState: Dictionary of buttons for the board squares.
    :return:
    """
    if gameData["Rpoints"] >= 12:
        gameData["playerWin"].grid(row=2, column=1)
        gameData["playerWinText"]["text"] = "Red wins!"
        gameData["playerWinText"]["foreground"] = "red"

        for key in boardState:
            buttonBoardState[key]["state"] = "disabled"

    elif gameData["Bpoints"] >= 12:
        gameData["playerWin"].grid(row=2, column=1)
        gameData["playerWinText"]["text"] = "Black wins!"

        for key in boardState:
            buttonBoardState[key]["state"] = "disabled"

def cleanHighlights(gameData, boardState, buttonBoardState):
    """
    Sets color and image of empty squares back to grey.
    :param gameData: Dictionary with all non piece related data.
    :param boardState: Main board state dictionary.
    :param buttonBoardState: Dictionary of buttons for the board squares.
    :return:
    """
    for key in boardState:
        if boardState[key] == "e":
            buttonBoardState[key]["image"] = Grey
            buttonBoardState[key]["bg"] = "grey"
            buttonBoardState[key]["command"] = partial(checkMove, key, gameData, boardState,
                                                       buttonBoardState)

def incrementScore(gameData):
    """
    Increments the score variable of the current player by one, and updates the corresponding score label to match.
    :param gameData: Dictionary with all non piece related data.
    :return:
    """
    if gameData["currentPlayer"] == 'r':
        gameData["Rpoints"] = gameData["Rpoints"] + 1
        gameData["RedScoreBoard"]["text"] = "Red Score: " + str(gameData["Rpoints"])
    elif gameData["currentPlayer"] == 'b':
        gameData["Bpoints"] = gameData["Bpoints"] + 1
        gameData["BlackScoreBoard"]["text"] = "Black Score: " + str(gameData["Bpoints"])

if __name__ == "__main__":
    myBoard = Board()
    myBoard.run()