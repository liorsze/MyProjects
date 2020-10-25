import sys
from random import randrange
import pygame
from config import *
from time import sleep

CHANGED = False


class Game:
    def __init__(self, screen):
        # initialize game board
        self.grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        self.score = 0
        self.best = 0
        self.font = pygame.font.SysFont("Gisha", 46, bold=True)
        self.screen = screen
        self.turn = False

    def initGrid(self):
        # put 2 twice on board in random location
        self.addTwoFour()
        self.addTwoFour()

    def addTwoFour(self):
        # 10% to put 4 on screen, 90% to put 2 on screen
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

    def restart(self, optional_best):
        # clear screen in order to play again
        global CHANGED
        self.grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        self.score = 0
        # store the best score so far
        if optional_best > self.best:
            self.best = optional_best
        CHANGED = False

    def printEnd(self, toPrint):
        # text is for winner/loser
        text_end = self.font.render(toPrint, 1, (0, 0, 0))
        self.screen.blit(text_end, (200, int(GAME_HEIGHT / 3)))
        # Ask user to play again
        self.screen.blit(self.font.render("Play again? (y/ n)", 1, (0, 0, 0)), (140, 255))
        pygame.display.update()
        sleep(2)
        # wait for user input

        run = True
        while run:
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_n):
                    run = False
                    # pygame.quit()
                    # sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    # 'y' is pressed to start a new game
                    self.restart(self.score)
                    # play again
                    self.playGame()

    def checkWinner(self):
        # if the board contain 2048 the user won
        if any(2048 in sublist for sublist in self.grid):
            winner = "You Won!!! :)"
            # print on screen
            self.printEnd(winner)
        else:
            # if not winner - check if loser
            self.checkLoser()

    def checkLoser(self):
        # the board is full
        if not any(0 in sublist for sublist in self.grid):
            loser = "You Lost! :("
            # print on screen
            self.printEnd(loser)

    def transpose(self):
        # switch rows and columns
        self.grid = [list(row) for row in zip(*self.grid)]

    def invert(self):
        # switch from right to left
        self.grid = [row[::-1] for row in self.grid]

    def notZero(self, row, col):
        # check that a cell value is different from 0
        return self.grid[row][col] != 0

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
        self.printBoard()
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
        # if the board changed in this turn, print 2/4 in random place
        if CHANGED:
            self.addTwoFour()

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

    def printBoard(self):
        # fill the entire screen with color
        self.screen.fill(tuple(color["background"]))

        # print score of current game
        score_str = "Score: " + str(self.score)
        text_score = self.font.render(score_str, 1, (0, 0, 0))
        self.screen.blit(text_score, (int(SCREEN_WIDTH / 8), 60))

        # print score of best game so far
        score_str = "Best: " + str(self.best)
        text_score = self.font.render(score_str, 1, (0, 0, 0))
        self.screen.blit(text_score, (int(SCREEN_WIDTH/2) + 80, 60))

        # size of one square on the board
        box = GAME_WIDTH // SIZE
        # print all squares
        for i in range(SIZE):
            for j in range(SIZE):
                box_color = tuple(color[str(self.grid[i][j])])
                pygame.draw.rect(self.screen, box_color, (50 + j * box + PADDING,
                                                          150 + i * box + PADDING,
                                                          box - 2 * PADDING,
                                                          box - 2 * PADDING), 0)
                # print number with colors
                if self.grid[i][j] != 0:
                    if self.grid[i][j] in (2, 4):
                        text_colour = tuple(color["dark"])
                    else:
                        text_colour = tuple(color["light"])
                    # display the number at the centre of the tile
                    self.screen.blit(self.font.render("{:>3}".format(
                        self.grid[i][j]), 1, text_colour),
                        # 5.5 and 7 were obtained by trial and error
                        (50 + j * box + 5.5 * PADDING, 150 + i * box + 7 * PADDING))
            pygame.display.update()

    def playGame(self):
        # initiate the game board
        global CHANGED
        self.initGrid()
        self.printBoard()

        running = True
        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    # Done! Time to quit.
                    running = False
                    # pygame.quit()
                    # sys.exit()

                # the user pressed an 'arrow' keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.moveUp()
                    if event.key == pygame.K_s:
                        self.moveDown()
                    if event.key == pygame.K_d:
                        self.moveRight()
                    if event.key == pygame.K_a:
                        self.moveLeft()
                    self.printBoard()
                CHANGED = False
                # there is 2048 on the board
                self.checkWinner()
