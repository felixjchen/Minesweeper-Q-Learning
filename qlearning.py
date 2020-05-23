import numpy as np 
from minesweeper import Minesweeper

env = Minesweeper(3, 1)

q_table = np.zeros((env.numStates, env.numMoves))
print(q_table.shape)