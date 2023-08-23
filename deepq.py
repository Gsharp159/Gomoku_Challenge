import tensorflow as tf
import gom_challenge as gom
from copy import deepcopy
import random as r
import numpy as np

q_network = tf.keras.Sequential([
    #state
    tf.keras.layers.Dense(169, activation=tf.nn.relu),
    tf.keras.layers.Dense(100, activation=tf.nn.relu),
    tf.keras.layers.Dense(100, activation=tf.nn.relu),
    tf.keras.layers.Dense(100, activation=tf.nn.relu),
    #q value every move
    tf.keras.layers.Dense(169)
])



def train():

    num_episodes = 3000
    epochs = 4
    epsilon = 0.5 #epsilon descent later
    opt = tf.keras.optimizers.legacy.Adam(learning_rate=0.001)

    q_network_w = tf.keras.models.load_model("models/dq_0.2_w", compile=False)
    q_network = tf.keras.models.load_model("models/dq_0.2", compile=False)

    state = deepcopy(gom.board)
    wins = 0
    games = 0



    for epoch in range(epochs):
        for episode in range(num_episodes):
            with tf.GradientTape() as tape:
                "Obtain Q-values from network"
                q_values = q_network_w((np.array(state).flatten()).reshape(1, 169))

                "Select action using epsilon-greedy policy"
                sample_epsilon = np.random.rand()
                if sample_epsilon <= epsilon: # Select random action
                    action = np.random.choice(169)
                else: # Select action with highest Q-value
                    action = np.argmax((q_values[0]))

                #action = (action // 13, action % 13)

                reward = 0
                moves = gom.pruneCoord(state)
                "Determine next state"
                if state[action // 13][action % 13] != 0:
                    reward = -5
                    move = r.choice(moves)
                    state[move[0]][move[1]] = -1
                else:
                    if episode != 0:
                        state[action // 13][action % 13] = 1
                    #player move here
                    #move = r.choice(gom.pruneCoord(state))
                    #state[move[0]][move[1]] = -1

                    move = np.argmax((q_values[0]))
                    state[move // 13][move % 13] = 1

                if episode % 100 == 0:
                    print(np.array(state))
                    print(episode)

                "Obtain Q-value for selected action"
                q_value = q_values[0][action]

                "Obtain direct reward for selected action"
                reward += 1 if (action // 13, action % 13) in moves else 0
                if gom.checkWin(1, state):
                    reward -= 10
                    wins += 1
                    games += 1
                    state = [[0 for i in range(13)] for k in range(13)]
                if gom.checkWin(-1, state):
                    reward += -10
                    games += 1
                    state = [[0 for i in range(13)] for k in range(13)]

                "Select next action with highest Q-value"
                if gom.pieces(1, state) + gom.pieces(-1, state) == 169:
                    next_q_value = 0 # No Q-value for terminal
                    state = [[0 for i in range(13)] for k in range(13)]
                    games += 1
                else:
                    next_q_values = tf.stop_gradient(q_network_w((np.array(state).flatten()).reshape(1, 169))) # No gradient computation
                    next_action = np.argmax(next_q_values[0])
                    next_q_value = next_q_values[0, next_action]

                "Compute observed Q-value"
                observed_q_value = reward + (gamma := 0.5 * next_q_value)

                "Compute loss value"
                loss_value = (observed_q_value - q_value)**2

                "Compute gradients"
                grads = tape.gradient(loss_value, q_network_w.trainable_variables)

                "Apply gradients to update network weights"
                opt.apply_gradients(zip(grads, q_network_w.trainable_variables))

        q_network_w.save("models/dq_0.2_w")
        q_network = tf.keras.models.load_model("models/dq_0.2")

        for episode in range(num_episodes):
            with tf.GradientTape() as tape:
                "Obtain Q-values from network"
                q_values = q_network((np.array(state).flatten()).reshape(1, 169))

                "Select action using epsilon-greedy policy"
                sample_epsilon = np.random.rand()
                if sample_epsilon <= epsilon: # Select random action
                    action = np.random.choice(169)
                else: # Select action with highest Q-value
                    action = np.argmax((q_values[0]))

                #action = (action // 13, action % 13)

                reward = 0
                moves = gom.pruneCoord(state)
                "Determine next state"
                if state[action // 13][action % 13] != 0:
                    reward = -5
                    move = r.choice(moves)
                    state[move[0]][move[1]] = 1
                else:
                    if episode != 0:
                        state[action // 13][action % 13] = 1
                    #player move here
                    move = r.choice(gom.pruneCoord(state))
                    state[move[0]][move[1]] = -1

                    #move = np.argmax((q_values_white[0]))
                    #state[move // 13][move % 13] = -1

                if episode % 100 == 0:
                    print(np.array(state))
                    print(episode)

                "Obtain Q-value for selected action"
                q_value = q_values[0][action]

                "Obtain direct reward for selected action"
                reward += 1 if (action // 13, action % 13) in moves else 0
                if gom.checkWin(1, state):
                    reward += 10
                    wins += 1
                    games += 1
                    state = [[0 for i in range(13)] for k in range(13)]
                if gom.checkWin(-1, state):
                    reward -= -10
                    games += 1
                    state = [[0 for i in range(13)] for k in range(13)]

                "Select next action with highest Q-value"
                if gom.pieces(1, state) + gom.pieces(-1, state) == 169:
                    next_q_value = 0 # No Q-value for terminal
                    state = [[0 for i in range(13)] for k in range(13)]
                    games += 1
                else:
                    next_q_values = tf.stop_gradient(q_network((np.array(state).flatten()).reshape(1, 169))) # No gradient computation
                    next_action = np.argmax(next_q_values[0])
                    next_q_value = next_q_values[0, next_action]

                "Compute observed Q-value"
                observed_q_value = reward + (gamma := 0.5 * next_q_value)

                "Compute loss value"
                loss_value = (observed_q_value - q_value)**2

                "Compute gradients"
                grads = tape.gradient(loss_value, q_network.trainable_variables)

                "Apply gradients to update network weights"
                opt.apply_gradients(zip(grads, q_network.trainable_variables))

        q_network.save("models/dq_0.2")

        print('BLACK WR', wins / games)
        print('EPOCH', epoch)


#train()

board = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

q_network = tf.keras.models.load_model("models/dq_0.2")
qvals = q_network(np.array(board).flatten().reshape(1, 169))
print(qvals)
action = np.argmax((qvals[0]))
print(action // 13, action % 13)

'''
res = tf.nn.softmax(model(np.array(board).flatten().reshape(1, 169)))
action = np.argmax(res[0])
aiMove = (action // 13, action % 13)
print(aiMove, (np.array(res)))
board[aiMove[0]][aiMove[1]] = 1
draw_window()
'''