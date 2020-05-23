import numpy as np
import os
import json
from pprint import pprint

MINE = -1
COVER = -2


class Minesweeper():

    def __init__(self, n=3, m=2):
        self.size = n
        self.mines = m
        self.maxTile = min(m, 8)

        self.stateEnumeration = {}
        self.max_states = len(self.stateEnumeration)
        self.getEnumeration()

        self.covers = []
        self.board = []
        self.newGame()

    def getEnumeration(self):
        n = self.size
        m = self.mines
        fname = f"{n}n{m}mEnumeration.json"
        if os.path.exists(fname):
            self.stateEnumeration = json.load(open(fname))
            print('LOADED ENUMERATION')
        else:
            print('BEGINING ENUMERATION')
            self.enumerateStates()
            json.dump(self.stateEnumeration, open(fname, 'w'), indent=4)
            print('DONE ENUMERATION')

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

        print('CREATED NEW GAME')

    def getStateNumber(self):

        n = self.size

        observedBoard = self.board[:]
        for i in range(n):
            for j in range(n):
                if self.covers[i][j]:
                    observedBoard[i][j] = COVER

        strEncodedBoard = ''
        for row in observedBoard:
            for j in row:
                strEncodedBoard += str(j)

        return self.stateEnumeration[strEncodedBoard]

    def move(action):

        # New enumerated state, reward for move, game status
        return newState, reward, status

    def __str__(self):
        r = ''

        n = self.size

        observedBoard = self.board[:]
        for i in range(n):
            for j in range(n):
                r += f'{self.board[i][j]}'
                # if self.covers[i][j]:
                #     r += 'X'
                # else:
                #     r += f'{self.board[i][j]}'
            r += '\n'

        return r


if __name__ == "__main__":
    m = Minesweeper(3, 2)
    print(m.getStateNumber())
    print(m)
