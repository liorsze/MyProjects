import sys
import pygame

# Import and initialize the pygame library
import MainBattleship
import MainHangman
import MainSnake
import Tetris
import Main2048

# Global vars
import TicTacToe

UP = False
DOWN = False
ENTER = False
CURRENT = 87
OFFSET = 35
GAMES = ["Tetris", "2048", "Hangman", "Battleship", "Tic-Tac-Toe", "Snake"]

# colors
white = (255, 255, 255)
black = (0, 0, 0)
dark_blue = (0, 0, 102)
offwhite = (200, 200, 200)
green = (0, 204, 0)


def draw_text_middle(surface, text, size, color, x, y):
    # write text in the middle of the screen
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (x - int(label.get_width() / 2), y - int(label.get_height() / 2)))


def printMenu(surf):
    surf.fill(white)
    # print pictures
    image_show = pygame.image.load('img/gamepic3.jpeg')
    surf.blit(image_show, (100, 0))
    draw_text_middle(surf, "Games Menu: ", 70, dark_blue, 315, 20)
    position = 90
    # print games
    for game in GAMES:
        draw_text_middle(surf, game, 35, offwhite, 300, position)
        position += OFFSET
    # print arrows
    draw_text_middle(surf, '>', 45, green, 190, CURRENT)
    draw_text_middle(surf, '<', 45, green, 410, CURRENT)
    pygame.display.flip()


def moveCursor():
    global CURRENT
    # move the cursor down
    if DOWN and CURRENT < 87+OFFSET*(len(GAMES) - 1):
        CURRENT += OFFSET
    # move the cursor up
    elif UP and 87 < CURRENT:
        CURRENT -= OFFSET
    # play the game
    elif ENTER:
        playGame()


def playGame():
    global ENTER
    # reset enter
    ENTER = False
    index = (CURRENT - 87) // 30
    game = GAMES[index]
    pygame.display.quit()
    # play games from the list
    if game == "2048":
        Main2048.start()
    elif game == "Tetris":
        Tetris.start()
    elif game == "Hangman":
        MainHangman.start()
    elif game == "Battleship":
        MainBattleship.start()
    elif game == "Tic-Tac-Toe":
        TicTacToe.start()
    elif game == "Snake":
        MainSnake.start()
    # print the menu again
    pygame.display.init()
    startMenu()


def startMenu():
    global DOWN, UP, ENTER

    # initialize
    pygame.init()
    surf = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Games Menu')

    # set title and icon
    pygame.display.set_caption("Games Menu")

    running = True

    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                # Done! Time to quit.
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    DOWN = True
                if event.key == pygame.K_UP:
                    UP = True
                if event.key == pygame.K_RETURN:
                    ENTER = True
        # print the menu
        printMenu(surf)
        # move the cursor up or down
        moveCursor()
        # reset values
        DOWN, UP = False, False

    # exit the menu
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    startMenu()
