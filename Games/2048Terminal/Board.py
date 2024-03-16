import os
from random import randrange

SIZE = 4
CHANGED = False


class Board:
    global SIZE

    def __init__(self):
        # initialize game board
        self.grid = [[0 for i in range(4)] for j in range(4)]
        self.score = 0
        self.winner = False

    def initGrid(self):
        # put 2 twice on board in random location
        self.addTwo()
        self.addTwo()

    def addTwo(self):
        new_elem = 4 if randrange(100) > 89 else 2
        # get random location on board
        row_index = randrange(SIZE - 1)
        col_index = randrange(SIZE - 1)
        # check if it's not in use
        while self.grid[row_index][col_index] != 0:
            row_index = randrange(SIZE)
            col_index = randrange(SIZE)
        # put 2 in the first found free random location
        self.grid[row_index][col_index] = new_elem

    def checkWinner(self):
        # if the board contain 2048 the user won
        if any(2048 in sublist for sublist in self.grid):
            self.winner = True

    def printGrid(self):
        # pretty print the board
        print(f'SCORE: {self.score}')
        for rows in self.grid:
            print(*['{:<5}'.format(each) for each in rows])

    def transpose(self):
        # switch rows and columns
        self.grid = [list(row) for row in zip(*self.grid)]

    def invert(self):
        # switch from right to left
        self.grid = [row[::-1] for row in self.grid]

    def notZero(self, row, col):
        # check that a cell value is different from 0
        return self.grid[row][col] != 0

    # def checkTurnHorizontal(self, col):
    #     for index in range(size):
    #         if self.grid[index][col] == 0:
    #             return True
    #
    # def checkTurnVertical(self, row):
    #     for index in range(size):
    #         if self.grid[row][index] == 0:
    #             return True

    def sumValues(self, row, col):
        global CHANGED
        if self.grid[row][col] == self.grid[row][col + 1]:
            # sum the values
            self.grid[row][col] *= 2
            # put 0 in the rightmost cell
            self.grid[row][col + 1] = 0
            # add sum to score
            self.score += self.grid[row][col]
            CHANGED = True

    def moveLeft(self):
        global CHANGED
        # run over the entire board
        for index_row in range(SIZE):
            for index_col in range(SIZE):
                # if the value of the cell is different form 0
                if self.notZero(index_row, index_col):
                    # if 2 neighbors cells have the same value - sum them
                    if index_col + 1 < SIZE:
                        self.sumValues(index_row, index_col)

                # the value of the cell is zero
                else:
                    tmp_col = index_col
                    # skip 0 and move values != 0 to the left
                    while tmp_col < SIZE and self.grid[index_row][tmp_col] == 0:
                        tmp_col += 1
                    if tmp_col < SIZE:
                        self.grid[index_row][index_col] = self.grid[index_row][tmp_col]
                        self.grid[index_row][tmp_col] = 0
                        CHANGED = True
                        # if 2 neighbors cells have the same value - sum them
                        if index_col - 1 >= 0:
                            self.sumValues(index_row, index_col - 1)
        if CHANGED:
            self.addTwo()

    def moveRight(self):
        # switch directions of the board
        self.invert()
        # call move left
        self.moveLeft()
        # switch directions again to the original
        self.invert()

    def moveUp(self):
        # flip the board top-bottom
        self.transpose()
        # call move left
        self.moveLeft()
        # flip again to the original
        self.transpose()

    def moveDown(self):
        # flip the board top-bottom
        self.transpose()
        # call move right
        self.moveRight()
        # flip again to the original
        self.transpose()

    def game(self):
        global CHANGED
        # initiate the game board
        self.initGrid()
        # while the board is not yet all covered - continue play
        while any(0 in sublist for sublist in self.grid):
            self.printGrid()
            turn = input('\ncommand are:\n'
                         'W to Move Up, S to Move Down\n'
                         'A to Move Left, D to Move Right\n'
                         'if you want to quit press Q\n')
            if turn == 'W' or turn == 'w':
                self.moveUp()
            elif turn == 'S' or turn == 's':
                self.moveDown()
            elif turn == 'A' or turn == 'a':
                self.moveLeft()
            elif turn == 'D' or turn == 'd':
                self.moveRight()
            # quit this round
            elif turn == 'Q' or turn == 'q':
                self.winner = True
                break
            else:
                print('invalid key, please try again...\n')
            # in order to create random 2 on board next turn
            CHANGED = False
            # there is 2048 on the board
            self.checkWinner()
            if self.winner:
                print('You Won!!!')
                break
            screen_clear()
        # the user lost
        if not self.winner:
            print('Game over...')


def screen_clear():
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows
        _ = os.system('cls')
