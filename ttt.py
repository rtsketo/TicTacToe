# Tic Tac Toe
import math
import random
import pygame

pygame.init()
screen = pygame.display.set_mode((564, 564))
pygame.display.set_caption("Tic Tac Toe")

O = pygame.image.load("circle.png")
X = pygame.image.load("cross.png")
win = pygame.image.load("win.png")
tie = pygame.image.load("tie.png")
loss = pygame.image.load("lose.png")

grid = [
    (30, 410), (220, 410), (410, 410),
    (30, 220), (220, 220), (410, 220),
    (30, 30), (220, 30), (410, 30)]


def clickedCell(pos):
    (mX, mY) = pos
    for i in range(len(grid)):
        (cX, cY) = grid[i]
        cX += 60;
        cY += 60
        # print((mX,mY,cX,cY,math.hypot(mX - cX, mY - cY)))
        if math.hypot(mX - cX, mY - cY) < 80:
            return i
    return -1


def drawBoard(board):
    # This function prints out the board that it was passed.
    # "board" is a list of 10 strings representing the board (ignore index 0)
    print(board[7] + '|' + board[8] + '|' + board[9])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[1] + '|' + board[2] + '|' + board[3])
    print()


def inputPlayerLetter(turn):
    # Lets the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print('Do you want to be X or O?')
        if turn == 'computer':
            letter = 'X'
        else:
            letter = 'O'
        print(letter)

    # the first element in the list is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or  # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or  # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or  # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or  # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le))  # diagonal


def getBoardCopy(board):
    # Make a copy of the board list and return it.
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy


def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '


def getPlayerMove(board):
    # Let the player type in their move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)


def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, computerLetter, i)
            if isWinner(boardCopy, computerLetter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, playerLetter, i)
            if isWinner(boardCopy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move is not None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


print('Welcome to Tic Tac Toe!')


def initGame():
    # Reset the board
    global theBoard, playerLetter, \
        computerLetter, gameIsPlaying, turn
    theBoard = [' '] * 10
    turn = whoGoesFirst()
    screen.fill((0, 0, 0))
    playerLetter, computerLetter = inputPlayerLetter(turn)
    screen.blit(pygame.image.load("grid.jpg"), (0, 0))
    print('The ' + turn + ' will go first.')
    pygame.display.flip()
    gameIsPlaying = True
    if turn == 'computer':
        advanceGame()


def displayMove(cell):
    if turn == 'player':
        img = X if playerLetter == 'X' else O
    else:
        img = X if computerLetter == 'X' else O
    screen.blit(img, grid[cell - 1])
    pygame.display.flip()


def displayOutcome(won=None):
    global gameIsPlaying
    img = tie if won is None else win if won else loss
    screen.blit(img, (564 / 2 - img.get_width() / 2,
                      564 / 2 - img.get_height() / 2))
    print('Do you want to play again? (yes or no)')
    pygame.display.flip()
    gameIsPlaying = False


def advanceGame(move=None):
    global gameIsPlaying, turn
    if gameIsPlaying:
        if turn == 'player' and move is not None:
            # Player's turn.
            # move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)
            displayMove(move)

            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                displayOutcome(True)
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    # break
                else:
                    turn = 'computer'

        else:
            # Computer's turn.
            cpu = getComputerMove(theBoard, computerLetter)
            if cpu is not None:
                makeMove(theBoard, computerLetter, cpu)
                drawBoard(theBoard)
                displayMove(cpu)

            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('The computer has beaten you! You lose.')
                displayOutcome(False)
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    displayOutcome()
                    # break
                else:
                    turn = 'player'


turn = ''
theBoard = []
playerLetter = ''
computerLetter = ''
initGame()

while True:
    global gameIsPlaying
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gameIsPlaying:
                cell = clickedCell(pygame.mouse.get_pos())
                if cell != -1 and isSpaceFree(theBoard, cell+1):
                    advanceGame(cell + 1)
                    if gameIsPlaying:
                        advanceGame()
            else:
                print('yes\n')
                initGame()
        if event.type == pygame.QUIT:
            raise SystemExit
