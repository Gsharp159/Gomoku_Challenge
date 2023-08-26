import tensorflow as tf
import numpy as np
import gomoku as gom_env

action_space = 169
observation_space = 169
tf.get_logger().setLevel('ERROR') # or INFO
tf.autograph.set_verbosity(3)

class DQN(tf.keras.Model):
    def __init__(self):
        super(DQN, self).__init__()
        self.d1 = tf.keras.layers.Dense(128, activation='relu')
        self.d2 = tf.keras.layers.Dense(128, activation='relu')
        self.v = tf.keras.layers.Dense(1, activation=None)
        self.a = tf.keras.layers.Dense(action_space, activation=None)

    def call(self, input_data):
        x = self.d1(input_data)
        x = self.d2(x)
        v = self.v(x)
        a = self.a(x)

        Q = v + (a - tf.math.reduce_mean(a, axis=1, keepdims=True))
        return Q
    
    def advantage(self, state):
        x = self.d1(state)
        x = self.d2(x)
        a = self.a(x)

        return a
    

class exp_replay():
    def __init__(self, buffer_size= 100000):
        self.buffer_size = buffer_size
        self.state_mem = np.zeros((self.buffer_size, observation_space), dtype=np.int32)
        self.action_mem = np.zeros((self.buffer_size), dtype=np.int32)
        self.reward_mem = np.zeros((self.buffer_size), dtype=np.float32)
        self.next_state_mem = np.zeros((self.buffer_size, observation_space), dtype=np.int32)
        self.done_mem = np.zeros((self.buffer_size), dtype=bool)
        self.pointer = 0

    def add_exp(self, state, action, reward, next_state, done):
        i = self.pointer % self.buffer_size
        self.state_mem[i] = state
        self.action_mem[i] = action
        self.reward_mem[i] = reward
        self.next_state_mem[i] = next_state
        self.done_mem[i] = 1 - int(done)
        self.pointer += 1

    def sample_exp(self, batch_size=64):
        max_mem = min(self.pointer, self.buffer_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)
        states = self.state_mem[batch]
        actions = self.action_mem[batch]
        rewards = self.reward_mem[batch]
        next_states = self.next_state_mem[batch]
        dones = self.done_mem[batch]

        return states, actions, rewards, next_states, dones

class agent():
    def __init__(self, gamma=0.99, replace=100, lr=0.0001):
        self.gamma = gamma
        self.epsilon = 1.0
        self.min_epsilon = 0.01
        self.epsilon_decay = 1e-3
        self.replace = replace
        self.trainstep = 0
        self.memory = exp_replay()
        self.batch_size = 64
        self.q_net = DQN()
        self.target_net = DQN()
        opt = tf.keras.optimizers.legacy.Adam(learning_rate=lr)
        self.q_net.compile(loss='mse', optimizer=opt)
        self.target_net.compile(loss='mse', optimizer=opt)


    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice([i for i in range(observation_space)])

        else:
            actions = self.q_net.advantage(np.array([state]))
            action = np.argmax(actions)
            return action

    def update_mem(self, state, action, reward, next_state, done):
        self.memory.add_exp(state, action, reward, next_state, done)

    def update_target(self):
        self.target_net.set_weights(self.q_net.get_weights())     

    def update_epsilon(self):
        self.epsilon = self.epsilon - self.epsilon_decay if self.epsilon > self.min_epsilon else self.min_epsilon
        return self.epsilon
    
    def train(self):
        if self.memory.pointer < self.batch_size:
            return 
        
        if self.trainstep % self.replace == 0:
            self.update_target()

        states, actions, rewards, next_states, dones = self.memory.sample_exp(self.batch_size)
        target = self.q_net.predict(states, verbose=0)
        next_state_val = self.target_net.predict(next_states, verbose=0)
        max_action = np.argmax(self.q_net.predict(next_states, verbose = 0), axis=1)
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        q_target = np.copy(target)  #optional  
        q_target[batch_index, actions] = rewards + self.gamma * next_state_val[batch_index, max_action] * dones
        self.q_net.train_on_batch(states, q_target)
        self.update_epsilon()
        self.trainstep += 1

    def save(self):
        self.q_net.save_weights("models/agent_black_0.1/")


black_agent = agent()
games = 100
results = []
for game in range(1, games):
    done = False
    state = gom_env.reset()
    total_reward = 0
    while not done:
        action = black_agent.act(state)

        next_state, reward, done = gom_env.black_step(action, state)

        black_agent.update_mem(state, action, reward, next_state, done)

        black_agent.train()

        state = next_state

        total_reward += reward
    
    if game % 15 == 0:
        print("LAST 15 AVERAGE SCORE: ", np.mean(results))
        results = []

    if done:
        results.append(total_reward)
        print("GAMES: {}/{} TOTAL REWARD: {} EPSILON: {}".format(game, games, total_reward, black_agent.epsilon))
        
black_agent.save()