import numpy as np
import json
import os
from pprint import pprint

MINE = -1
COVER = -2

np.random.seed(0)


class Minesweeper():

    def __init__(self, n=3, m=2):
        self.size = n
        self.mines = m
        # Largest number tile
        self.maxTile = min(m, 8)

        # Create game
        self.newGame()

        # Load in state enumeration
        self.getEnumeration()
        self.numStates = len(self.stateEnumeration)
        self.numMoves = n **2

        print('INIT COMPLETE')

    def getEnumeration(self):
        n = self.size
        m = self.mines
        fname = f"data/{n}n{m}mEnumeration.json"
        if os.path.exists(fname):
            self.stateEnumeration = json.load(open(fname))
        else:
            self.enumerateStates()
            json.dump(self.stateEnumeration, open(fname, 'w'), indent=4)

    def enumerateStates(self):
        n = self.size
        m = self.mines

        i = 0

        # DFS is cheaper on memmory
        stack = [('', 0)]
        while stack:

            j, length = stack.pop()

            if length == n ** 2:
                # print(i / ((3 + self.maxTile) ** (n ** 2)) * 100, j)
                self.stateEnumeration[j] = i
                i += 1
            else:
                for k in range(-2, self.maxTile + 1):
                    stack += [(f'{j}{k}', length + 1)]

    def newGame(self):
        n = self.size
        m = self.mines

        self.covers = [[1 for _ in range(n)] for _ in range(n)]
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.squaresLeft = (n**2) - m

        # Place mines
        for i in np.random.choice(n**2, m, replace=False):
            self.board[i // n][i % n] = MINE

        # Paint numbers
        for i in range(n):
            for j in range(n):

                if self.board[i][j] != MINE:
                    count = 0

                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if 0 <= i + di <= n - 1 and 0 <= j + dj <= n-1:

                                if self.board[i+di][j+dj] == MINE:
                                    count += 1

                    self.board[i][j] = count

    def getState(self):

        n = self.size

        strEncodedBoard = ''
        for i in range(n):
            for j in range(n):
                if self.covers[i][j]:
                    strEncodedBoard += str(COVER)
                else:
                    strEncodedBoard += str(self.board[i][j])

        print(strEncodedBoard)

        return self.stateEnumeration[strEncodedBoard]

    def move(self, action):
        n = self.size

        i, j = action // n, action % n

        # Already uncovered...
        if self.covers[i][j] == 0:
            # Small penalty for wasting time
            reward = -1
            done = False
        else:
            self.covers[i][j] = 0

            if self.board[i][j] == MINE:
                reward = - (n**3)
                done = True
            else:
                # Small penalty for wasting time
                reward = -1
                done = False

                self.squaresLeft -= 1
                if self.squaresLeft == 0:
                    reward = (n**3)
                    done = True

        # New enumerated state, reward for move, game done
        newState = self.getState()
        return newState, reward, done

    def __str__(self):
        r = ''

        n = self.size

        for i in range(n):
            for j in range(n):
                if self.covers[i][j]:
                    r += 'X'
                else:
                    r += f'{self.board[i][j]} '
            r += '\n'
        return r


if __name__ == "__main__":
    m = Minesweeper(3, 1)
    print('# of states:', m.numStates)

    print(m.getState())
    print(m.move(0))
    print(m.move(1))
    print(m.move(2))
    print(m.move(3))
    print(m.move(4))
    print(m.move(5))
    print(m.move(6))
    print(m.move(8))
