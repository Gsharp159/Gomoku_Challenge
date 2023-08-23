import numpy as np
import random as rand

board_size = 13
board = [[0 for i in range(board_size)] for j in range(board_size)]

def getBoard():
    return board

#x, y in array format, color 1 = black color 2 = white
def place(x, y, color):
    if board[x][y] == 0:
        board[x][y] = color
        return True
    else:
        return False
    
    #checkWinCon
def getColumn(index):
    col = [0] * 13

    for i in range(board_size):
        col[i] = board[i][index]

    return col

def getPD(index):
    arr = np.array(board)
    return np.diag(arr, index)

def getND(index):
    arr = np.array(board)
    return np.diag(np.fliplr(arr), index)

def checkWin(color):
    #check vert
    for ind in range(board_size):
        column = getColumn(ind)

        for i in range(board_size - 4):
            sequential = 0

            for c in range(0, 5):
                if column[i + c] == color:
                    sequential += 1
                else:
                    break

            if (sequential == 5):
                return True

    #check horiz
    for row in board:

        for i in range(board_size - 4):
            sequential = 0

            for c in range(0, 5):
                if row[i + c] == color:
                    sequential += 1
                else:
                    break
            
            if (sequential == 5):
                return True

    #check positive diag
    for ind in range((-board_size - 1), (board_size - 1)):
        line = getPD(ind)

        if len(line) < 5:
            continue
        else:
            for i in range(len(line) - 4):
                sequential = 0

                for c in range(0, 5):
                    if line[i + c] == color:
                        sequential += 1
                    else:
                        break
            
                if (sequential == 5):
                    return True

    #check negative diag
    for ind in range((-board_size - 1), (board_size - 1)):
        line = getND(ind)

        if len(line) < 5:
            continue
        else:
            for i in range(len(line) - 4):
                sequential = 0

                for c in range(0, 5):
                    if line[i + c] == color:
                        sequential += 1
                    else:
                        break
            
                if (sequential == 5):
                    return True

def handPlay():
    turns = 0
    while (not(checkWin(1) or checkWin(2))):
        if (turns % 2) == 0:
            x = int(input('(BLACK) Select X: '))
            y = int(input('(BLACK) Select Y: '))
            place(x, y, 1)
        else:
            x = int(input('(WHITE) Select X: '))
            y = int(input('(WHITE) Select Y: '))
            place(x, y, 2)

        turns += 1

        print(np.array(board))

    if ((turns - 1) % 2) == 0:
        print('Black Won')
    else:
        print('White Won')

def randPlay():
    turns = 0

    global board
    board = [[0 for i in range(board_size)] for j in range(board_size)]

    while (not(checkWin(1) or checkWin(2))):
        if (turns % 2) == 0:
            while True:
                x = rand.randint(0,12)
                y = rand.randint(0,12)
                if place(x, y, 1):
                    break
        else:
            while True:
                x = rand.randint(0,12)
                y = rand.randint(0,12)
                if place(x, y, 2):
                    break

        turns += 1

    #print(np.array(board))

    if ((turns - 1) % 2) == 0:
        #print('Black Won')
        return 1
    else:
        #print('White Won')
        return 2

    
def simPlay(games):
    white = 0
    black = 0
    for i in range(games):
        print(str(i) + '/' + str(games))
        game = randPlay()

        if game == 1:
            black += 1
        
        if game == 2:
            white += 1

    print ('black wr: ' + str((black / games) * 100) + '%')

