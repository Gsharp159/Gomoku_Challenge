from Gomoku import *
from copy import deepcopy

#This is more a wrapper for alphabeta() which is the actual minimax. Iterates every space and returns the minimax score
def minimax(color, _board, _depth=3):
    max = True if color == 1 else False
    values = []
    temp = copy(_board)
    coords = pruneCoord(temp)
    for i, k in coords:
        print((i, k), coords)
        temp[i][k] = color
        values.append([(i, k), alphabeta(color, temp, depth=_depth)])
        temp[i][k] = 0
    
    values = sorted(values, key=lambda x: x[1], reverse=max)
    #values_cull = [move for move in values if move[1] == values[0][1]] #filter out all moves that dont give best score 

    print(values)
    return values[0]
    #return rand.choice(options_culled)

#minimax with alpha beta pruning, no iterative deepening
def alphabeta(color, _board, alpha=-100, beta=100, depth=2):

    temp_board = copy(_board)
    #v = pruneCoord(temp_board)
    v = [a[0] for a in evaluateMoves(temp_board)][0:10]

    if depth == 0 or (checkWin(1, _board) or checkWin(-1, _board)):
        return score(_board)
    if color == 1:
        value = -100
        for coords in v:
            temp_board[coords[0]][coords[1]] = color
            value = max(value, alphabeta(-1, temp_board, depth=depth-1))
            temp_board[coords[0]][coords[1]] = 0
            if value > beta:
                break
            alpha = max(alpha, value)
        return value
    else:
        value = 100
        for coords in v:
            temp_board[coords[0]][coords[1]] = color
            value = min(value, alphabeta(1, temp_board, depth=depth-1))
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

def MCTS(color, _board, process_length=5):
    available_moves = pruneCoord(_board)
    results = [(0, 0) for i in range(len(available_moves))]

    #initialize all of em
    for i, k in available_moves:
        temp = deepcopy(_board)
        temp[i][k] = color

        p = playout(temp, color)
        if color == p:
            results[available_moves.index((i, k))][0] += 1
            results[available_moves.index((i, k))][1] += 1
        else:
            results[available_moves.index((i, k))][1] += 1




    #once initialized, pick best one and go from there

    #update

    #is there a better first move? try this one etc
