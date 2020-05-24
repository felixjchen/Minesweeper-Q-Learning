import numpy as np
import matplotlib.pyplot as plt
from minesweeper import Minesweeper

np.random.seed(0)


class QLearning():

    def __init__(self, size=3, mines=1, alpha=0.25, gamma=0.3, epsilon=0.15):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.env = Minesweeper(size, mines)
        self.q_table = np.zeros((self.env.numStates, self.env.numMoves))

    def train(self, epochs=1000):
        """
        Trains model and returns win percentage over epochs. 
        """
        
        alpha = self.alpha
        gamma = self.gamma
        epsilon = self.epsilon
        env = self.env
        q_table = self.q_table

        wins = 0

        for _ in range(epochs):

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
        Gets win percentage of model over trials. Model repeating action counts as a lose. Model losing on first choice is not counted as lose.
        """

        env = self.env
        q_table = self.q_table

        wins = 0
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
                    reward = -1
                    done = True
                # First turn lose
                if done and moves == 0 and reward < 0:
                    instantLoses += 1

                # Win
                if done and reward > 0:
                    wins += 1

                state = newState
                moves += 1

        return wins / (trials - instantLoses) * 100

def graph():
    xs = [i/100 for i in range(1, 100)]
    training = []
    testing = []

    for x in xs:
        print(int(x * 100))
        model = QLearning(size=3, mines=2, gamma=x)
        training += [model.train(10000)]
        testing += [model.test(100)]

    plt.plot(xs, training, label="Training")
    plt.plot(xs, testing, label="Testing")
    plt.xlabel('Hyperparameter')
    plt.ylabel('Win Percentage')
    plt.title('gamma')
    plt.legend()
    plt.savefig('graphs/gamma.png')
    plt.show()

if __name__ == "__main__":
    model = QLearning(size=3, mines=2,)
    trainWP = model.train(100000)
    testWP = model.test(1000)

    print(f'Training win percentage: {trainWP}')
    print(f'Testing win percentage: {testWP}')