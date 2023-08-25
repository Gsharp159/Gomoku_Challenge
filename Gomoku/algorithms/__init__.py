#import sys; sys.path.append('/Users/Gage/Desktop/Code/Python/Gomoku')
from gomoku import *
from copy import deepcopy
import math
import time

local_board = [
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

def MCTS(color, _board, iterations=10):

    class MCTS_Node():

        def __init__(self, arg_board, n_color=color, parent=None):
            self.parent = parent
            self.node_color = n_color
            self.arg_board = arg_board
            self.wins = 0
            self.games = 0
            self.available_moves = pruneCoord(self.arg_board)
            self.results = [[0, 0] for i in range(len(self.available_moves))]
            self.children = [None for i in range(len(self.available_moves))]

            #On birth of node, playout each available move
            for i, k in self.available_moves:
                temp = [i[:] for i in self.arg_board]
                temp[i][k] = self.node_color

                p = playout(temp, self.node_color * -1)

                if self.node_color == p:
                    self.results[self.available_moves.index((i, k))][0] += 1
                    self.results[self.available_moves.index((i, k))][1] += 1
                    self.games += 1
                else:
                    self.results[self.available_moves.index((i, k))][1] += 1
                    self.wins += 1
                    self.games += 1


        def addChild(self, obj, index):
            self.children[index] = obj

        def getNextMove(self, as_index=False):

            UCT = []
            c = 1.5

            for w, g in self.results:
                UCT.append((w / g) + (c * (math.log(self.wins)/g)))

            if as_index:
                return np.argmax(UCT)
            else:
                return self.available_moves[np.argmax(UCT)]
            
        def getMostGames(self):
            return self.available_moves[np.argmax([g for w, g in self.results])]
        
        def getBestChild(self):
            #print([(w / g) for w, g in self.results])
            return self.children[np.argmax([(w / g) if g != 0 else 0 for w, g in self.results])]
        
        def getNextState(self):
            temp_2 = [i[:] for i in self.arg_board]
            move = self.getNextMove()
            temp_2[move[0]][move[1]] = self.node_color
            return temp_2
        
        def getParent(self):
            return self.parent
        
        def isTerminal(self):
            return (not self.available_moves) or checkWin(1, self.arg_board) or checkWin(-1, self.arg_board)
        
        def backprop(self, WLtuple):
            self.wins += WLtuple[1] - WLtuple[0]
            self.games += WLtuple[1]

            ind = self.getNextMove(as_index=True)

            self.results[ind][0] += WLtuple[0]
            self.results[ind][1] += WLtuple[1]

            if self.parent != None:
                self.parent.backprop(WLtuple)
        
    #make this the actual main func and move class to outside func
    #main first node
    root = MCTS_Node(_board)
    def mcts_drive(node, a_board):
        if node.isTerminal():
            if checkWin(node.node_color, node.arg_board):
                node.backprop((1, 1))
                return
            else:
                node.backprop((0, 1))
                return

        #establish working node
        if node.getBestChild() == None: #This node has been generated but doesn't have children
            newchild = MCTS_Node(node.getNextState(), n_color=node.node_color * -1, parent=node)
            node.addChild(newchild, node.getNextMove(as_index=True))
            node.backprop((newchild.wins, newchild.games))
        else: #This node was generated and has a child of its own
            child = node.getBestChild()
            mcts_drive(child, node.getNextState()) #keep going until node without children (i.e leaf)



    
    start = time.time()
    for i in range(iterations):
        mcts_drive(root, _board)
    end = time.time()
    print('ITERATIONS:', iterations)
    print('AVERAGE ITERATION TIME:', (end - start)/iterations)

    return root.getMostGames()


if __name__ == '__main__':

    print(MCTS(-1, local_board))
