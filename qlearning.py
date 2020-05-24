import numpy as np
from minesweeper import Minesweeper

np.random.seed(0)

ALPHA = 0.3
GAMMA = 0.9
EPSILON = 0.2

EPOCHS = 100000

env = Minesweeper(3, 1)
q_table = np.zeros((env.numStates, env.numMoves))
# print(q_table.shape)

wins = 0

for e in range(EPOCHS):

    state = env.newGame()
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


print('TRAINING DONE')
print(wins/EPOCHS * 100)

# TEST
# state = env.newGame()
# done = False
# while not done:
#     action = np.argmax(q_table[state])

#     newState, reward, done = env.move(action)

#     state = newState

#     print(env)
