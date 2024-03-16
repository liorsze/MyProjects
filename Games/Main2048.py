import pygame
from config import *
from Game2048 import Game
from time import sleep

from MainHangman import blit_text

# Import and initialize the pygame library
pygame.init()
myfont = pygame.font.SysFont("Century Schoolbook", 24)


def startGame(screen):
    # set title and icon
    pygame.display.set_caption("2048")
    icon = pygame.image.load("img/2048_logo.png")
    pygame.display.set_icon(icon)

    # fill the window screen with brownies background
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    surf.fill(color["over"])
    screen.blit(surf, (0, 0))

    # welcome text to the user
    text = 'Welcome to 2048!\n\n' \
           'Your goal is to create the number 2048 by sliding the numbers on the grid\n' \
           'command are:\n'\
           'W to Move Up\n' \
           'S to Move Down\n'\
           'A to Move Left\n' \
           'D to Move Right\n' \
           'if you want to quit press Q\n\n'\
           'Good Luck! :) \n'

    # print on screen
    blit_text(screen, text, (70, 20), myfont)
    pygame.display.update()
    sleep(3)

    # initialize the game and run it
    board = Game(screen)
    board.playGame()


def start():
    # Set up the drawing window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    startGame(screen)
