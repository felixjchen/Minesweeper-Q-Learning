import numpy as np
import matplotlib.pyplot as plt
import sys

from minesweeper import Minesweeper

np.random.seed(0)

class QLearning():

    def __init__(self, size=3, mines=2, alpha=0.05, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.env = Minesweeper(size, mines)
        self.q_table = np.zeros((self.env.numStates, self.env.numMoves))

    def train(self, epochs=1000):
        """
        Trains function and returns win percentage over epochs. 
        """

        alpha = self.alpha
        gamma = self.gamma
        epsilon = self.epsilon
        env = self.env
        q_table = self.q_table

        wins = 0

        for e in range(epochs):

            sys.stdout.write(
                f'\rEpoch {round((e+1)/(epochs+1) * 100, 2)}% WR {round(wins / epochs * 100, 2)}%')
            sys.stdout.flush()

            state = self.env.newGame()
            done = False

            while not done:

                if np.random.uniform(0, 1) < epsilon:
                    action = np.random.randint(0, env.numMoves)
                else:
                    action = np.argmax(q_table[state])

                newState, reward, done = env.move(action)

                oldReward = q_table[state, action]
                nextMax = np.argmax(q_table[newState])

                # UPDATE
                q_table[state, action] = (1-alpha)*oldReward + \
                    alpha*(reward + gamma*nextMax)

                # MOVE
                state = newState

                if done and reward > 0:
                    wins += 1

        return wins / epochs * 100

    def test(self, trials=100):
        """
        Gets win percentage of function over trials. Repeating action counts as a lose. Losing on first choice is not counted as lose.
        """

        env = self.env
        q_table = self.q_table

        wins = 0
        penalties = 0
        instantLoses = 0

        for _ in range(trials):
            state = env.newGame()
            done = False
            moves = 0
            # print('NEWGAME')
            while not done:
                action = np.argmax(q_table[state])

                newState, reward, done = env.move(action)

                # Repeat action autofail
                if state == newState:
                    reward = -999
                    penalties += 1
                    done = True

                # First turn lose
                if done and moves == 0 and reward < 0:
                    instantLoses += 1

                # Win
                if done and reward > 0:
                    wins += 1

                state = newState
                moves += 1

                # print(env)

        return wins / (trials - instantLoses) * 100, penalties 


def graph():
    xs = [i/100 for i in range(1, 100)]
    training = []
    testing = []

    for x in xs:

        sys.stdout.write(
            f'\rDone {x*100}%')
        sys.stdout.flush()

        model = QLearning(size=4, mines=2, epsilon=x)
        training += [model.train(1000000)]
        testing += [model.test(10000)[0]]

    plt.plot(xs, training, label="Training")
    plt.plot(xs, testing, label="Testing")
    plt.xlabel('Hyperparameter')
    plt.ylabel('Win Percentage')
    plt.title('epsilon')
    plt.legend()
    plt.savefig('graphs/epsilon.png')
    # plt.show()


if __name__ == "__main__":
    graph()
    # size=3, mines=2, alpha=0.05, gamma=0.9, epsilon=0.1
    # size=4, mines=1, alpha=0.3, gamma=0.95, epsilon=0.1

    # SIZE = 4
    # MINES = 2
    # ALPHA = 0.2
    # GAMMA = 0.9
    # EPSILON = 0.1
    # model = QLearning(SIZE, MINES, ALPHA, GAMMA, EPSILON)
    # trainWP = model.train(1000000)
    # testWP, penalties = model.test(10000)

    # print('')
    # print(f'Training win percentage: {trainWP}')
    # print(f'Testing win percentage: {testWP} with {penalties} penalties')
