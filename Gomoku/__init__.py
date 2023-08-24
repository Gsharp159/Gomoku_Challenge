import numpy as np
import random as rand
import pygame as pg
import random as r
import time
from pygame.locals import *
import itertools, operator
from copy import *

BOARD_SIZE = 13

#This exists for debugging
board = [
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
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

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

            else:
                #
                #Case: block detect False, incomplete
                #
                pass

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
    return (longestSequential(color, board) == 5)

#TODO if no pieces, return all
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
def pieces(color, _board):
    count = 0

    for i in range(BOARD_SIZE):
        for k in range(BOARD_SIZE):
            if _board[i][k] == color:
                count += 1
    
    return count

#The scoring function for minimax
def score(_board):
    if checkWin(-1, _board):
        return -1000
    if checkWin(1, _board):
        return 1000

    return longestSequential(1, _board) - longestSequential(-1, _board)

def playout(_board, color):
    if color == 1:
        tcount = 0
    else:
        tcount = 1
    temp_board = np.copy(_board)
    while not(checkWin(1, temp_board) or checkWin(-1, temp_board)):
        moves = pruneCoord(temp_board)
        player = ((tcount % 2) * 2) - 1
        if not moves:
            return 0
        move = r.choices(moves)[0]
        temp_board[move[0]][move[1]] = player
        tcount += 1

    return ((((tcount - 1) % 2) * 2) - 1) #temp_board

def randState(_board, max):
    tcount = 0
    temp_board = np.copy(_board)
    while (not(checkWin(1, temp_board) or checkWin(-1, temp_board))) and tcount != r.randint(1, max):
        moves = pruneCoord(temp_board)
        player = ((tcount % 2) * 2) - 1
        if not moves:
            return (temp_board, 0)
        move = r.choices(moves)[0]
        temp_board[move[0]][move[1]] = player
        tcount += 1

    toPlay = ((tcount % 2) * 2) - 1
    return (temp_board, toPlay)

#in the name
#needs to be updated?
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
def evaluateMoves(_board, coords=True, onPiece=False):

    l_board = copy(_board)

    #TODO fix inefficiency, checks pieces multiple times and overwrites their chain lengths

    moves = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    #pieces = pieceLocations(_board, False, 1)


    #start = tuple coord, direction = tuple difference
    def isChain(start, direction, n=1):
        if max(start[0], start[1]) == BOARD_SIZE - 1 or min(start[0], start[1]) == 0:
            return n
        elif l_board[start[0] + direction[0]][start[1] + direction[1]] != 0:
            return isChain((start[0] + direction[0], start[1] + direction[1]), direction, n+1)
        else:
            return n

    #does a piece have a pieve next to it? does that piece have a piece next to it? if chain more that threshold, go to piece 1 and go opposite direction
    #if this itself isnt efficient enough, could try running only on pruned coords
    if onPiece:
        for i in range(BOARD_SIZE ** 2):
            coord = (i // BOARD_SIZE, i % BOARD_SIZE)
            possible_moves = []
            for z in range(-1, 2):
                for w in range(-1, 2):
                    if l_board[coord[0]][coord[1]] != 0 and (not (max(coord[0] + z, coord[1] + w) > BOARD_SIZE - 1 or min(coord[0] + z, coord[1] + w) < 0)) and l_board[coord[0] + z][coord[1] + w] != 0 and (not z == w == 0):
                        possible_moves.append(isChain((coord[0] + z, coord[1] + w), (z, w)) + 1)
            moves[coord[0]][coord[1]] = max(possible_moves) if possible_moves else 0

    else:
        for i in range(BOARD_SIZE ** 2):
            coord = (i // BOARD_SIZE, i % BOARD_SIZE)
            for z in range(-1, 2):
                for w in range(-1, 2):
                    if not (max(coord[0], coord[1]) == BOARD_SIZE - 1 or min(coord[0], coord[1]) == 0):
                        if l_board[coord[0] + z][coord[1] + w] != 0 and (not z == w == 0) and (l_board[coord[0]][coord[1]] == 0):
                            moves[coord[0]][coord[1]] = isChain((coord[0] + z, coord[1] + w), (z, w))

    if coords:
        moves = [[(i // BOARD_SIZE, i % BOARD_SIZE), moves[i // BOARD_SIZE][i % BOARD_SIZE]] for i in range(BOARD_SIZE ** 2)]
        moves = sorted(moves, key=lambda x: x[1], reverse=True)

    return moves

def threatSpace(_board, color):
    #? uh? same as isChain in evaluateMoves, but rather than checking consecutive, check specific patterns
    #open 4

    #single block 4

    #open 3

    #broken 3
    return None

def linesAnalysis(_board, color):
    #should lines be weighted differently for threat/ non threat (i.e built out of opposite vs self color)
    #coefficient of chainlength
    #coefficient per player
    #add lines vs chain coefficient

    _board = deepcopy(_board)
    pieces = pieceLocations(_board)
    lines = [[0 for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    chains = evaluateMoves(_board, coords=False, onPiece=True)

    #hard to program this efficiently oopsie, stamp arrays kinda thing?
    for x, y in pieces:
        for i in reversed(range(1, 5)):
            change = chains[x][y] if chains[x][y] > 0 else 1 * (5 - i)#(chains[x][y] if chains[x][y] > 0 else 1) * i


            if (x - i) >= 0:
                lines[x - i][y] += change

                if y + i < BOARD_SIZE:
                    lines[x - i][y + i] += change

                if y - i >= 0:
                    lines[x - i][y - i] += change

            if x + i < BOARD_SIZE:
                lines[x + i][y] += change

                if y + i < BOARD_SIZE:
                    lines[x + i][y + i] += change

                if y - i >= 0:
                    lines[x + i][y - i] += change

            if y - i >= 0:
                lines[x][y - i] += change

            if y + i < BOARD_SIZE:
                lines[x][y + i] += change

    for x, y in pieces:
        lines[x][y] = 0

    return lines

#print(np.array(board))
#print(np.array(evaluateMoves(board, coords=False, onPiece=True)))
#print(np.array(linesAnalysis(board, 0)))

def place(color, coord):
    board[coord[0]][coord[1]] = color

def placeAiMove(color, _board, func):
    aiMove = func(color, _board)
    place(color, aiMove)
            

