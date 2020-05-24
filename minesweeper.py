import numpy as np
import json
import os

MINE = -1
COVER = -2


class Minesweeper():

    def __init__(self, n=3, m=2):
        """
        An nxn minesweeper board with m mines

        n -- length of side
        m -- number of mines
        """
        self.size = n
        self.mines = m
        # Largest number tile
        self.maxTile = min(m, 8)

        # Load in state enumeration
        self.stateEnumeration = {}
        self.getEnumeration()
        self.numStates = len(self.stateEnumeration)
        self.numMoves = n ** 2

        # Create game
        self.newGame()

    def getEnumeration(self):
        """ Gets an enumeration of states into memmory, load if cached else create. """
        n = self.size
        m = self.mines
        fname = f"data/{n}n{m}mEnumeration.json"

        if not os.path.exists(fname):
            self.cacheEnumeration(fname)

        self.stateEnumeration = json.load(open(fname))['enumeration']

    def cacheEnumeration(self, fname, batchsize=1000):
        """ 
        DFS to get all possible states.

        There are n^2 cells.
        Each cell can take on 1 (bomb) + 1 (cover) + 0-8 (number of surrounding bombs) states.
        => 11^(n^2) states, yikes.

        Can reduce the base by using the number of bombs as the maximum number of surrounding bombs, i.e our tile numbers are in [0, min(m, 8)].
        => (3 + min(m, 8))^(n^2)

        If DFS can't handle the memmory required for the string encoded boards, then its infeasble to store every string encoded board anyways.
        """
        # Create file
        json.dump({
            'enumeration': {},
            'stack': []
        }, open(fname, 'w'), indent=4)

        n = self.size
        m = self.mines

        i = 0

        # DFS is cheaper on memmory
        stack = [('', 0)]
        batch, b = {}, 0
        while stack:

            j, length = stack.pop()

            if length == n ** 2:

                batch[j] = i

                # Append batch
                if b > 100000 or i == (3 + self.maxTile) ** (n ** 2) - 1:
                    print(f'{int(i / ((3 + self.maxTile) ** (n ** 2)) * 100)} %', j)
                    data = json.load(open(fname, "r"))
                    data['enumeration'].update(batch)
                    data['stack'] = stack
                    json.dump(data, open(fname, "w"), indent=4)

                    batch, b = {}, 0

                b += 1
                i += 1
            else:
                for k in range(-2, self.maxTile + 1):
                    stack += [(f'{j}{k}', length + 1)]

    def newGame(self):
        """ Starts a new game of minesweeper """
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

        return self.getState()

    def getState(self):
        """ Returns the state number for the current state of the gmae"""
        n = self.size

        strEncodedBoard = ''
        for i in range(n):
            for j in range(n):
                if self.covers[i][j]:
                    strEncodedBoard += str(COVER)
                else:
                    strEncodedBoard += str(self.board[i][j])

        return self.stateEnumeration[strEncodedBoard]

    def move(self, action):
        """ 
        Takes action and returns new state number, reward and if the game is finished

        action -- uncover board at row action // 2 and col action % 2
        """
        n = self.size

        i, j = action // n, action % n

        # Already uncovered...
        if self.covers[i][j] == 0:
            # penalty for wasting time
            reward = -n
            done = False
        else:
            self.covers[i][j] = 0

            if self.board[i][j] == MINE:
                reward = - (n**3)
                done = True
            else:
                reward = 2
                done = False

                self.squaresLeft -= 1
                if self.squaresLeft == 0:
                    reward = (n**3)
                    done = True

        # New enumerated state, reward for move, game done
        return self.getState(), reward, done

    def __str__(self):
        """ Returns a str representation of the board """
        r = ''

        n = self.size

        for i in range(n):
            for j in range(n):
                if self.covers[i][j]:
                    r += 'X  '
                else:
                    t = str(self.board[i][j])
                    t = t+' ' if len(t) == 2 else t + '  '
                    r += f'{t}'
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
