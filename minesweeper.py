import numpy as np

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
        self.numStates = (3 + self.maxTile) ** (n ** 2)
        self.numMoves = n ** 2

        # Create game
        self.newGame()

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
        """
        Return the state number for the current self.board. We treat every cell as it's own digit in base 11. This way each board state has a unique state number.

        base 11? 
        1 (cover) + 1 (bomb) + 0-8 (tile numbers) => each tile has 11 states

        We can try to cut corners on the largest tile number = min(# of bombs, 8)

        base 3 + self.maxTile?
        1 (cover) + 1 (bomb) + 0-min(# of bombs, 8) (tile numbers) => each tile has 3+maxTile states
        """
        n = self.size

        decimal = 0
        base = 3+self.maxTile
        for i in range(n**2):
            # Our state number is the observed state, we need to worry about what is covered
            # Shift right by two since we have -2 for covered and -1 for bomb => 0-10 digit
            if self.covers[i // n][i % n] == 1:
                digit = COVER + 2
            else:
                digit = self.board[i // n][i % n] + 2

            decimal += digit * (base ** i)

        return decimal

    def move(self, action):
        """ 
        Takes action and returns new state number, reward and if the game is finished

        action -- uncover board at row (action//2) and column (action%2)
        """
        n = self.size

        i, j = action // n, action % n

        # Already uncovered...
        if self.covers[i][j] == 0:
            # penalty for wasting time
            reward = - n ** 2
            done = False
        else:
            # Sweep
            self.covers[i][j] = 0

            # Lose
            if self.board[i][j] == MINE:
                reward = - n ** 4
                done = True
            else:
                reward = n
                done = False
                self.squaresLeft -= 1

                # Win
                if self.squaresLeft == 0:
                    reward = n ** 3
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
