##monte carlo, then save each state and probability, train tensorflow model to predict winner, then use the model rather than 
#random playouts. Would speed up other algos and reduce depth? monte carlo also is better than minimax anyway
import gom_challenge as gom
import random as r
import numpy as np
import csv
import copy

board = np.array([
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
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
'''
def recur(_board):
    possible_moves = gom.pieceLocations(_board)
    layer = [move, 0 for move in possible_moves]

'''







'''
class Tree():

    wins = 0
    games = 0
    player = 1

    def __init__(self, root):
        self.root = root
        self.children = []
        self.Nodes = []

    def addNode(self, obj):
        self.children.append(obj)

    def getAllNodes(self):
        self.Nodes.append(self.root)
        for child in self.children:
            self.Nodes.append(child.data)
        for child in self.children:
            if child.getChildNodes(self.Nodes) != None:
                child.getChildNodes(self.Nodes)
        print(*self.Nodes, sep = "\n")
        print('Tree Size:' + str(len(self.Nodes)))

    def migrate(self):
        pass

class Node():
    def __init__(self, title, color, local_board):
        self.title = title
        self.local_board = local_board
        self.moves = {m : False for m in gom.pruneCoord(local_board)}
        self.movecount = len(self.moves)
        self.children = []
        self.games = 0
        self.wins = 0
        self.color = color

    def addNode(self, m, obj):
        self.children.append(obj)
        self.moves[m] = True

    def getChildNodes(self, Tree):
        for child in self.children:
            if child.children:
                child.getChildNodes(Tree)
                Tree.append(child.data)
            else:
                Tree.append(child.data)

    def getLeaves(self):
        res = []
        for move in moves:
            if not move[1]:
                res.append(move[0])
'''
'''
#get parent info method
class Node():

    children = {}
    wins = 0
    games = 0

    def __init__(self, board_state, move, color, parent):
        self.board_state = copy.deepcopy(board_state)
        self.color = color
        self.move = move
        self.parent = parent

    def addChild(self, obj):
        self.children[obj.move] = obj

    def getParent(self):
        return self.parent

    def getAll(self):
        pass






mom = Node(board, None, 1, None)
temp = copy.deepcopy(board)
temp[0][0] = 1
mom.addChild(Node(temp, (0, 0), 1, mom))
temp[0][1] = -1
mom.children[(0, 0)].addChild(Node(temp, (0, 1), -1, mom.children[(0, 0)]))

print([(key, value) for (key, value) in mom.children])
a = Node(temp, (0, 3), 1, mom.children[(0, 0)])
print(a.getParent().move)
'''


'''
tree = Tree('bossman')

tree.addNode(Node('district mgr a'))
tree.addNode(Node('district mgr b'))

tree.children[0].addNode(Node('jeni sluttery'))

tree.children[0].children[0].addNode(Node('PATRICK'))

tree.getAllNodes()
'''

#1) select child node from root (current state) until you reach an unplayed state
#2) choose a random child of this leaf node (play random move)
#3) play it out randomly with random moves
#4) backpropogate to the root, and add one to every node on the paths game count, and 1 only if it was the winning player

# some way of selecting a good move vs an exploratory move -> epsilon decay
# for now, random





#board = root
#select a random move
def playout(_board, color):
    if color == 1:
        tcount = 0
    else:
        tcount = 1
    temp_board = np.copy(_board)
    while not(gom.checkWin(1, temp_board) or gom.checkWin(-1, temp_board)):
        moves = gom.pruneCoord(temp_board)
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
    while (not(gom.checkWin(1, temp_board) or gom.checkWin(-1, temp_board))) and tcount != r.randint(1, max):
        moves = gom.pruneCoord(temp_board)
        player = ((tcount % 2) * 2) - 1
        if not moves:
            return (temp_board, 0)
        move = r.choices(moves)[0]
        temp_board[move[0]][move[1]] = player
        tcount += 1

    toPlay = ((tcount % 2) * 2) - 1
    return (temp_board, toPlay)



with open('data.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, lineterminator='\n', delimiter=',')

    for i in range(200000):
        row = []
        state = randState(board, 24)

        flat = np.array(state[0]).flatten()

        for n in flat:
            row.append(n)

        p = playout(state[0], state[1])

        row.append(1 if p == 1 else 0)
        row.append(1 if p == 0 else 0)
        row.append(1 if p == -1 else 0)#[1, 0] if p == 1 else [0, 1])

        csvwriter.writerow(row)
        if (i % 1000 == 0):
            print(i, '/', '200')


'''
#-------------

def search(node):
    #if node is win/lose:
        #backprop

    if not node.getLeaves():
        #not a leaf so search child for leaf
        #'best' = most game count
        best = (None, 0)
        for child in node.children:
            #games played to start but change to stats/ prob
            if child.games > best[1]:
                best = (child, child.games)
        search(best[0])

    else:
        #was a leaf!
        available_moves = []
        for m in node.moves:
            if not m[1]:
                available_moves.append(m[0])

        move = random.choice(available_moves)
        new_board = np.copy(node.local_board)
        new_board[move[0]][move[1]] = node.color * -1

        node.addNode(Node('titel', node.color * -1, new_board))

        result = playout(new_board, node.color * -1)




        #play random
        #backprop

def search(node):
'''

