import numpy as np
import random as rand
import pygame as pg
import sys
import time
from pygame.locals import *

board_size = 13
board = [[0 for i in range(board_size)] for j in range(board_size)]

#x, y in array format, color 1 = black color -1 = white
def place(x, y, color):
    if board[x][y] == 0:
        board[x][y] = color
    else:
        pass


def checkWin(color, board):
    def getPD(index):
        arr = np.array(board)
        return np.diag(arr, index)

    def getND(index):
        arr = np.array(board)
        return np.diag(np.fliplr(arr), index)
    #check vert
    for ind in range(board_size):
        column = [board[i][ind] for i in range(board_size)]

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
    return False

board = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

#print(checkWin(1, board))

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

    #resize
    intiating_window = pg.transform.scale(intiating_window, (width, height))
    black_img = pg.transform.scale(black_img, (35, 35))
    white_img = pg.transform.scale(white_img, (35, 35))
    board_image = pg.transform.scale(board_image, (650, 650))

    def game_initiating_window():
        #screen.blit(intiating_window, (0, 0))

        pg.display.update()
        #time.sleep(0.5)
        screen.fill(black)

        draw_window()

    def draw_window():

        screen.blit(board_image, ((width / 2) - 500, (height / 2) - 325))

        message = 'play da game b'

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


        for i in range(13):
            for k in range(13):
                if board[i][k] == 0:
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
        if board[coords[0]][coords[1]] == -1:
            aiTurn = False
        board[coords[0]][coords[1]] = -1
        draw_window()

        ###ai func here for now rand caveman
        while aiTurn:
            x = rand.randint(0, 12)
            y = rand.randint(0, 12)
            if board[x][y] == 0:
                board[x][y] = 1
                break


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