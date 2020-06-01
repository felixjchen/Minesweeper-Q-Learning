import numpy as np
import matplotlib.pyplot as plt
import sys

from minesweeper import Minesweeper

np.random.seed(0)


class QLearning():

    def __init__(self, size, mines, reward_profile, alpha=0.05, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.env = Minesweeper(size, mines, reward_profile)
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
                nextMax = np.max(q_table[newState])

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

                # print(env)
                moves += 1
                state = newState

        return wins / (trials - instantLoses) * 100, penalties

    def demo(self):
        env = self.env
        q_table = self.q_table

        state = env.newGame()
        done = False
        while not done:
            action = np.argmax(q_table[state])

            newState, reward, done = env.move(action)

            # Repeat action autofail
            if state == newState:
                reward = -999
                done = True

            state = newState

            print(env)
            if done and reward > 0:
                print('WIN')
            elif done:
                print('LOSE')


def graph():
    xs = [i/1000 for i in range(1, 1000)]
    training = []
    testing = []

    for x in xs:

        sys.stdout.write(
            f'\rDone {x*100}%')
        sys.stdout.flush()

        reward_profile = {
            'sweep': 1,
            'resweep': -2,
            'win': 4 ** 2,
            'lose': -4 ** 2
        }

        model = QLearning(4, 2, reward_profile, gamma=x)
        training += [model.train(30000)]
        testing += [model.test(10000)[0]]

    plt.plot(xs, training, label="Training")
    plt.plot(xs, testing, label="Testing")
    plt.xlabel('Hyperparameter')
    plt.ylabel('Win Percentage')
    plt.title('gamma')
    plt.legend()
    plt.savefig('graphs/gamma.png')
    # plt.show()


if __name__ == "__main__":
    # graph()
    SIZE = 4
    MINES = 2
    ALPHA = 0.05
    GAMMA = 0.95
    EPSILON = 0.1
    reward_profile = {
        'sweep': 1,
        'resweep': -2,
        'win': SIZE ** 2,
        'lose': -SIZE ** 2
    }
    model = QLearning(SIZE, MINES, reward_profile, ALPHA, GAMMA, EPSILON)
    trainWP = model.train(150000)
    testWP, penalties = model.test(10000)

    print('')
    print(f'Training win percentage: {trainWP}')
    print(f'Testing win percentage: {testWP} with {penalties} penalties')
