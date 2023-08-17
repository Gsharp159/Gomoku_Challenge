import numpy as np
import random as rand
import pygame as pg
import sys
import time
from pygame.locals import *
import itertools, operator
from copy import copy

BOARD_SIZE = 13

#This exists for debugging
board = [
[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
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
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

#Returns the longest sequence of pieces for a given color. 'block_detect' determines whether it overrides blocked sequences to zero
def longestSequential(color, board, block_detect=True):
    def getPD(index):
        arr = np.array(board)
        return np.diag(arr, index)

    def getND(index):
        arr = np.array(board)
        return np.diag(np.fliplr(arr), index)
    
    #Defined so it didn't need to be rewritten 4 times for horiz, vert, etc
    def checkLine(line, bd=block_detect, _color=color):
        if (_color in line) and (len(line) > 0):
            r = max((list(y) for (x,y) in itertools.groupby((enumerate(line)),operator.itemgetter(1)) if x == _color), key=len)

            if bd:
                if (r[0][0] > 0):
                    l_blocked = (column[r[0][0] - 1] == (_color * -1))
                else:
                    l_blocked = True

                if (r[-1][0] != (BOARD_SIZE - 1)):
                    r_blocked = (column[r[-1][0] + 1] == (_color * -1))
                else:
                    r_blocked = True

                if not (l_blocked and r_blocked):
                    sequential = (r[-1][0] - r[0][0]) + 1 if (r[-1][0] - r[0][0]) + 1 > sequential_vert else sequential_vert
                else:
                    #sub = line[0:r[0][0]] + line[r[-1][0] + 1:-1]
                    sub = list(copy(line))
                    if (r[0][0]-r[-1][0]) > 0:
                        for i in range(r[0][0], r[-1][0] + 1):
                            sub.pop(i)
                        sequential = checkLine(sub, bd)
                    else:
                        sequential = 0

                return sequential
        return 0

    #check vert
    sequential_vert = 0
    for ind in range(BOARD_SIZE):
        column = [board[i][ind] for i in range(BOARD_SIZE)]
        if (Length := checkLine(column, block_detect, color)) > sequential_vert:
            sequential_vert = Length

    #check horiz
    sequential_hor = 0
    for row in board:
        if (Length := checkLine(row, block_detect, color)) > sequential_hor:
            sequential_hor = Length

    #check positive diag
    sequential_pd = 0
    for ind in range((-BOARD_SIZE - 1), (BOARD_SIZE - 1)):
        line = getPD(ind)
        if (Length := checkLine(line, block_detect, color)) > sequential_pd:
            sequential_pd = Length

    #check negative diag
    sequential_nd = 0
    for ind in range((-BOARD_SIZE - 1), (BOARD_SIZE - 1)):
        line = getND(ind)
        if (Length := checkLine(line, block_detect, color)) > sequential_nd:
            sequential_nd = Length


    return (max(sequential_hor, sequential_vert, sequential_pd, sequential_nd))

#Returns whether a color has won or not
def checkWin(color, board):
    #In the official gomoku rules, a run longer than 6 does not qualify a win. However, I am not a prude
    return (longestSequential(color, board) >= 5)

#Returns all positions on the board that are adjacent to an already placed piece for either player as an array of booleans
def prune(_board):

    valid = [[False for i in range(BOARD_SIZE)] for k in range(BOARD_SIZE)]

    for i in range(BOARD_SIZE):
        for k in range(BOARD_SIZE):
            if _board[i][k] == 0:
                continue
            else:
                for z in range(-1, 2):
                    for w in range(-1, 2):
                        if (i+z < 0) or (i+z > BOARD_SIZE-1) or (k+w < 0) or (k+w > BOARD_SIZE-1):
                            continue
                        elif _board[i+z][k+w] == 0:
                            valid[i+z][k+w] = True
    
    return valid

#The same as prune, but returns only the array coordinates of valid moves
def pruneCoord(_board):

    valid = []

    for i in range(BOARD_SIZE):
        for k in range(BOARD_SIZE):
            if _board[i][k] == 0:
                continue
            else:
                for z in range(-1, 2):
                    for w in range(-1, 2):
                        if (i+z < 0) or (i+z >= BOARD_SIZE) or (k+w < 0) or (k+w >= BOARD_SIZE):
                            continue
                        elif _board[i+z][k+w] == 0:
                            valid.append((i+z, k+w))
    
    return valid

#returns the total piece count for either player
#Probably useless, only temporary as I haven't implemented a turn counter yet
def pieces(color):
    count = 0

    for i in range(BOARD_SIZE):
        for k in range(BOARD_SIZE):
            if board[i][k] == color:
                count += 1
    
    return count

#The scoring function for minimax
def score(_board):
    if checkWin(-1, _board):
        return -1000
    if checkWin(1, _board):
        return 1000

    return longestSequential(1, _board) - longestSequential(-1, _board)

def pieceLocations(_board, all=True, color=0):

    coords = []
    _board = np.array(_board)
    unpacked = _board.flatten()

    if all or color == 0:
        for i in range(len(unpacked)):
            if unpacked[i] != 0:
                coords.append((i // BOARD_SIZE, i % BOARD_SIZE))
    else:
        for i in range(len(unpacked)):
            if unpacked[i] == color:
                coords.append((i // BOARD_SIZE, i % BOARD_SIZE))

    return coords

#return moves that are part of a consecutive chain of either players pieces, or any fatal moves
def evaluateMoves(_board):
    #does a piece have a pieve next to it? does that piece have a piece next to it? if chain more that threshold, go to piece 1 and go opposite direction
    #if this itself isnt efficient enough, could try running only on pruned coords
    pieces = pieceLocations(_board, False, 1)
    for coord in pieces:
        #if nearby piece in direction
            #if that direction on nearby piece, etc (recursion orrrrrr?)
    pass

evaluateMoves(board)

#This is more a wrapper for alphabeta() which is the actual minimax. Iterates every space and returns the minimax score
def minimax(color, _board, _depth=3):
    max = True if color == 1 else False
    values = []
    temp = copy(_board)
    coords = pruneCoord(temp)
    for i, k in coords:
            temp[i][k] = color
            values.append([(i, k), alphabeta(color, temp, depth=_depth)])
            temp[i][k] = 0
    
    values = sorted(values, key=lambda x: x[1], reverse=max)
    values_cull = [move for move in values if move[1] == values[0][1]] #filter out all moves that dont give best score 

    print(values)
    return values[0]
    #return rand.choice(options_culled)

#minimax with alpha beta pruning, no iterative deepening
def alphabeta(color, _board, alpha=-100, beta=100, depth=2):

    temp_board = copy(_board)
    v = pruneCoord(temp_board)

    if depth == 0 or (checkWin(1, _board) or checkWin(-1, _board)):
        return score(_board)
    if color == 1:
        value = -100
        for coords in v:
            temp_board[coords[0]][coords[1]] = color
            value = max(value, alphabeta(color * -1, temp_board, depth=depth-1))
            temp_board[coords[0]][coords[1]] = 0
            if value > beta:
                break
            alpha = max(alpha, value)
        return value
    else:
        value = 100
        for coords in v:
            temp_board[coords[0]][coords[1]] = color
            value = min(value, alphabeta(color * -1, temp_board, depth=depth-1))
            temp_board[coords[0]][coords[1]] = 0
            if value < alpha:
                break
            beta = min(beta, value)
        return value

#Early on algorithm for the bot, mostly for debugging
def lengthOptimizer(color, _board):

    options = []

    test_board = copy(_board)
    for i in range(BOARD_SIZE):
        for k in range(BOARD_SIZE):
            if board[i][k] == 0:
                test_board[i][k] = color
                options.append([(i, k), score(test_board)])
                test_board[i][k] = 0

    options = sorted(options, key=lambda x: x[1], reverse=True)
    options = [move for move in options if move[1] == options[0][1]]

    return rand.choice(options)[0]

class Game():

    #
    # 0 -> empty space, 1 -> black, -1 -> white
    #

    BOARD_SIZE = 13
    board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

    def __init__(self, bot_func, player=1):
        print('init mate')
        self.bot_func = bot_func
        self.player = player

    def getBoard():
        return board
    
    def place(color, coords):
        board[coords[0]][coord[1]] = color

    def generateMove():
        pass
            

