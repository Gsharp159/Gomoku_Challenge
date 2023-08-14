import numpy as np
import random as rand
import pygame as pg
import sys
import time
from pygame.locals import *
import itertools, operator
from copy import copy

board_size = 13
board = [[0 for i in range(board_size)] for j in range(board_size)]

def longestSequential(color, board, block_detect=True):
    def getPD(index):
        arr = np.array(board)
        return np.diag(arr, index)

    def getND(index):
        arr = np.array(board)
        return np.diag(np.fliplr(arr), index)
    
    def checkLine(line, bd=block_detect, _color=color):
        if (_color in line) and (len(line) > 0):
            r = max((list(y) for (x,y) in itertools.groupby((enumerate(line)),operator.itemgetter(1)) if x == _color), key=len)

            if bd:
                if (r[0][0] > 0):
                    l_blocked = (column[r[0][0] - 1] == (_color * -1))
                else:
                    l_blocked = True

                if (r[-1][0] != (board_size - 1)):
                    r_blocked = (column[r[-1][0] + 1] == (_color * -1))
                else:
                    r_blocked = True

                if not (l_blocked and r_blocked):
                    sequential = (r[-1][0] - r[0][0]) + 1 if (r[-1][0] - r[0][0]) + 1 > sequential_vert else sequential_vert
                else:
                    sub = line[0:r[0][0]] + line[r[-1][0] + 1:-1]
                    sequential = checkLine(sub, bd)

                return sequential
        return 0

    #check vert
    sequential_vert = 0
    for ind in range(board_size):
        column = [board[i][ind] for i in range(board_size)]
        if (Length := checkLine(column, block_detect, color)) > sequential_vert:
            sequential_vert = Length

    #check horiz
    sequential_hor = 0
    for row in board:
        if (Length := checkLine(row, block_detect, color)) > sequential_hor:
            sequential_hor = Length

    #check positive diag
    sequential_pd = 0
    for ind in range((-board_size - 1), (board_size - 1)):
        line = getPD(ind)
        if (Length := checkLine(line, block_detect, color)) > sequential_pd:
            sequential_pd = Length

    #check negative diag
    sequential_nd = 0
    for ind in range((-board_size - 1), (board_size - 1)):
        line = getND(ind)
        if (Length := checkLine(line, block_detect, color)) > sequential_nd:
            sequential_nd = Length
            
    return (max(sequential_hor, sequential_vert, sequential_pd, sequential_nd))

def checkWin(color, board):
    if longestSequential(color, board) >= 5:
        return True
    else:
        return False

board = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

print(longestSequential(-1, board, True))
#print(longestSequential(1, board))
#print(checkWin(1, board))


def prune(_board):

    valid = [[False for i in range(board_size)] for k in range(board_size)]

    for i in range(board_size):
        for k in range(board_size):
            if _board[i][k] == 0:
                continue
            else:
                for z in range(-1, 2):
                    for w in range(-1, 2):
                        if _board[i+z][k+w] == 0:
                            valid[i+z][k+w] = True
    
    return valid

def score(_board):
    if checkWin(-1, _board):
        return -1000
    if checkWin(1, _board):
        return 1000

    return longestSequential(1, _board) - longestSequential(-1, _board)

def minimax(color, _board, depth=2):
    options = []
    max = True if color == 1 else False

    v = prune(_board)

    test_board = copy(_board)
    for i in range(board_size):
        for k in range(board_size):
            if not v[i][k] or _board[i][k] != 0:
                continue
            else:
                test_board[i][k] = color
                local_score = minimax(color*-1, test_board, depth-1)[1] if depth != 0 else score(test_board)
                options.append([(i, k), local_score])
                test_board[i][k] = 0

    options = sorted(options, key=lambda x: x[1], reverse=max)
    options_culled = [move for move in options if move[1] == options[0][1]] #filter out all moves that dont give best score

    print(options_culled)
    return options_culled[0]
    #return rand.choice(options_culled)

def lengthOptimizer(color, _board):

    options = []

    test_board = copy(_board)
    for i in range(board_size):
        for k in range(board_size):
            if board[i][k] == 0:
                test_board[i][k] = color
                options.append([(i, k), score(test_board)])
                test_board[i][k] = 0

    options = sorted(options, key=lambda x: x[1], reverse=True)
    options = [move for move in options if move[1] == options[0][1]]

    return rand.choice(options)[0]

##### below this is draft for pygame
def GUIWindow():
    width = 1200
    height = 800
    white = (255, 255, 255)
    black = (0, 0, 0)
    fps = 30
    CLOCK = pg.time.Clock()

    pg.init()
    screen = pg.display.set_mode((width, height), 0, fps)
    pg.display.set_caption("shut up")

    intiating_window = pg.image.load("Assets/photo_five_comp.jpg")
    black_img = pg.image.load("Assets/black_stone.png")
    white_img = pg.image.load("Assets/white_stone.png")
    board_image = pg.image.load("Assets/board_image.png")
    green_square = pg.image.load("Assets/green.png")

    #resize
    intiating_window = pg.transform.scale(intiating_window, (width, height))
    black_img = pg.transform.scale(black_img, (35, 35))
    white_img = pg.transform.scale(white_img, (35, 35))
    board_image = pg.transform.scale(board_image, (650, 650))
    green_square = pg.transform.scale(green_square, (10, 10))

    def game_initiating_window():
        #screen.blit(intiating_window, (0, 0))

        #pg.display.update()
        #time.sleep(0.5)
        screen.fill(black)

        draw_window()

    def draw_window():

        screen.blit(board_image, ((width / 2) - 500, (height / 2) - 325))

        message = str(longestSequential(1, board, block_detect=False))

        if checkWin(1, board):
            message = 'Black takes the dub'
        if checkWin(-1, board):
            message = 'white *fortnite dance*'

        font = pg.font.Font(None, 40)

        text = font.render(message, 1, black)

        screen.fill(white, ((width / 2) + 200, 75, 350, 75))
        text_rect = text.get_rect(center=((width / 2) + 375, 115))
        screen.blit(text, text_rect)

        draw_board()

        pg.display.update()

    def draw_board():
        #first row is 87, last is 677.5 dif is 45.4
        #first col is 112, last is 702.5
        #row * 45.4 + 87 ? smth like this

        v = prune(board)

        for i in range(13):
            for k in range(13):
                if board[i][k] == 0:
                    if v[i][k]:
                        screen.blit(green_square, ((i * 49.2) + 125, (k * 49.2)+ 100))
                    continue
                if board[i][k] == -1:
                    screen.blit(white_img, ((i * 49.2) + 112, (k * 49.2)+ 87))
                if board[i][k] == 1:
                    screen.blit(black_img, ((i * 49.2) + 112, (k * 49.2)+ 87))


    def user_click():

        first = (112, 87)
        last = (737.5, 702.5)

        x, y = pg.mouse.get_pos()
        coords = [0, 0]

        if not ((x >= 112) and (x <= 737.5)):
            pass#raise Exception('ur only allowed to click the board rn bb')
        else:
            x = (x - 112)
            x = round(x / (625.5 / 12))

            coords[0] = x

        if not ((y >= 87) and (y <= 737.5)):
            pass#raise Exception('ur only allowed to click the board rn bb')
        else:
            y = (y - 87)
            y = round(y / (625.5 / 12))

            coords[1] = y

        aiTurn = True
        if board[coords[0]][coords[1]] != 0:
            aiTurn = False
        else:
            board[coords[0]][coords[1]] = -1
        draw_window()

        if aiTurn:
            ###ai func
            #aiMove = lengthOptimizer(1, board)
            aiMove = minimax(1, board, 1)[0]
            print(aiMove)
            board[aiMove[0]][aiMove[1]] = 1
            draw_window()

    game_initiating_window()

    while(True):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if any(pg.mouse.get_pressed()):
                user_click()

                if(False):
                    reset_game()

        draw_window()
        pg.display.update()
        CLOCK.tick(fps)

GUIWindow()