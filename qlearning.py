import numpy as np
from minesweeper import Minesweeper

np.random.seed(0)

class QLearning():
    
    def __init__(self, size=3, mines=1, ALPHA=0.1, GAMMA=0.9, EPSILON=0.1):
        self.ALPHA = ALPHA
        self.GAMMA = GAMMA 
        self.EPSILON = EPSILON

        self.env = Minesweeper(size, mines)
        self.q_table = np.zeros((self.env.numStates, self.env.numMoves))

    def train(self, epochs=1000):
        ALPHA = self.ALPHA
        GAMMA = self.GAMMA
        EPSILON = self.EPSILON
        env = self.env
        q_table = self.q_table

        wins = 0

        for _ in range(epochs):

            state = self.env.newGame()
            done = False

            while not done:

                if np.random.uniform(0, 1) < EPSILON:
                    action = np.random.randint(0, env.numMoves)
                else:
                    action = np.argmax(q_table[state])

                newState, reward, done = env.move(action)

                oldReward = q_table[state, action]
                nextMax = np.argmax(q_table[newState])

                # UPDATE
                q_table[state, action] = (1-ALPHA)*oldReward + \
                    ALPHA*(reward + GAMMA*nextMax)

                # MOVE
                state = newState

                if done:
                    if reward > 0:
                        wins += 1

        return wins / epochs * 100

    def test(self, trials = 100):
        env = self.env
        q_table = self.q_table
        wins = 0

        for _ in range(trials):
            state = env.newGame()
            done = False

            while not done:
                if np.random.uniform(0, 1) < 0.0001:
                    action = np.random.randint(0, env.numMoves)
                else:
                    action = np.argmax(q_table[state])

                newState, reward, done = env.move(action)

                state = newState

                if done:
                    if reward > 0:
                        wins += 1

        return wins / trials * 100


model = QLearning(size=3, mines=1)
print(model.train(10000))
print('TRAINING DONE')
print(model.test(100))
print('TESTING DONE')

