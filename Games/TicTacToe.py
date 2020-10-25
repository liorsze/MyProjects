import sys
import pygame
import random
from time import sleep
from GamesMenu import draw_text_middle


class Grid:
    def __init__(self):
        self.grid_lines = [((0, 200), (600, 200)),  # horizon 1
                           ((0, 400), (600, 400)),  # horizon 2
                           ((200, 0), (200, 600)),  # vertical 1
                           ((400, 0), (400, 600))]  # vertical 2

    def draw(self, surface):
        # draw on screen the game grid
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)


class Button:
    def __init__(self, x, y, surf, width, text=''):
        self.visible = True
        self.x = x
        self.y = y
        self.width = width
        self.color = (153, 255, 255)
        self.text = text
        self.surf = surf

    def draw(self):
        # draw button on screen
        pygame.draw.rect(self.surf, (255, 255, 255), pygame.Rect(self.x, self.y, self.width, 55))
        font = pygame.font.SysFont('Goudy Old Style', 30, bold=True)
        text = font.render(self.text, 1, (255, 0, 0))
        self.surf.blit(text, (self.x + 35, 210))


# Global vars
top_left_x = 300
top_left_y = 300
grid = Grid()
board = ['', '', '',
         '', '', '',
         '', '', '', ]
board_tuples = [(40, 40), (241, 40), (441, 40),
                (40, 241), (241, 241), (441, 241),
                (40, 441), (241, 441), (441, 441)]

pygame.init()
pygame.display.set_caption('Tic-Tac-Toe')


def startGame(surface):
    run = True
    # 1 = X , 0 = O
    game_mode, player1, player2 = -1, -1, -1

    # color screen black
    surface.fill((0, 0, 0))
    chooseMode(surface)

    while run:
        for event in pygame.event.get():
            # the user want to quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                run = False

            # get mouse positions
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # get user choice - play against computer or another player
                if game_mode == -1 and 120 < mouse_x < 300 and 200 < mouse_y < 255:
                    game_mode = 1
                elif game_mode == -1 and 320 < mouse_x < 500 and 200 < mouse_y < 255:
                    game_mode = 2
                elif player1 == -1 and player2 == -1 and game_mode != -1:
                    if 170 < mouse_x < 260 and 200 < mouse_y < 255:
                        player1, player2 = 1, 0
                    elif 370 < mouse_x < 460 and 200 < mouse_y < 255:
                        player1, player2 = 0, 1

            # if game mode was chosen, choose user symbol
            if game_mode != - 1 and player1 == -1 and player2 == -1:
                surface.fill((0, 0, 0))
                chooseSymbol(surface)

            # if symbols were chosen - start the game
            if player1 != -1 and player2 != -1:
                surface.fill((0, 0, 0))
                printBoard(surface)
                pygame.display.flip()
                # game logic
                run = game(surface, game_mode, player1, player2)

    # clean screen before exit
    reset(surface)


def game(surface, mode, player1, player2):
    # player vs. computer
    if mode == 1:
        return playersGame(surface, player1, player2, True)
    # player1 vs player2
    elif mode == 2:
        return playersGame(surface, player1, player2, False)


def playersGame(surface, player1, player2, computer):
    win = False
    ret = True
    # for each turn, up to 9
    for i in range(9):
        # 'even' player turn
        if i % 2 == 0:
            # choose where to put symbol
            ret_turn = turn(player1)
            if not ret_turn:
                return False
            # print game board after choice
            printBoard(surface)
            # check if there are 3 from same symbol in a row
            win = checkBordForWin(player1)
            if win:
                # print message on screen - end of game
                ret = printScreen(surface, "player1 has won!!!")
                break
        else:
            # if user play with computer
            if computer:
                computerTurn(player1, player2)
            # if user play with another user
            else:
                ret_turn = turn(player2)
                if not ret_turn:
                    return False
            printBoard(surface)
            # check if there are 3 from same symbol in a row
            win = checkBordForWin(player2)
            if win:
                if computer:
                    # print message on screen - end of game
                    ret = printScreen(surface, "You lose..")
                else:
                    # print message on screen - end of game
                    ret = printScreen(surface, "player1 has won!!!")
                break
    if not win:
        # print message on screen - end of game
        ret = printScreen(surface, "Its a tie!!")
    return ret


def turn(player):
    position = -1
    ret = True
    while position == -1:
        for event in pygame.event.get():
            # the user want to quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                return False

            # get mouse positions
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # check where the user mouse clicked and get the block number from it
                if 0 < mouse_x < 200 and 0 < mouse_y < 200:
                    if board[0] == '':
                        position = 0
                elif 201 < mouse_x < 400 and 0 < mouse_y < 200:
                    if board[1] == '':
                        position = 1
                elif 401 < mouse_x < 600 and 0 < mouse_y < 200:
                    if board[2] == '':
                        position = 2
                elif 0 < mouse_x < 200 and 201 < mouse_y < 400:
                    if board[3] == '':
                        position = 3
                elif 201 < mouse_x < 400 and 201 < mouse_y < 400:
                    if board[4] == '':
                        position = 4
                elif 401 < mouse_x < 600 and 201 < mouse_y < 400:
                    if board[5] == '':
                        position = 5
                elif 0 < mouse_x < 200 and 401 < mouse_y < 600:
                    if board[6] == '':
                        position = 6
                elif 201 < mouse_x < 400 and 401 < mouse_y < 600:
                    if board[7] == '':
                        position = 7
                elif 401 < mouse_x < 600 and 401 < mouse_y < 600:
                    if board[8] == '':
                        position = 8
    # put symbol in board
    board[position] = player
    return True


def computerTurn(player1, player2):
    corners = [0, 2, 6, 8]
    sides = [1, 3, 5, 7]
    sleep(0.5)
    center = 4
    # first check if cp win next turn
    block = checkIfPlayerWinsNextTurn(player2)
    if block != -1:
        board[block] = player2
    else:
        # check if player win next turn and block him
        block = checkIfPlayerWinsNextTurn(player1)
        if block != -1:
            board[block] = player2
        else:
            # try to catch a corner
            block = computerTurnLogic(player2, corners)
            if block == -1:
                # try center
                if board[center] == '':
                    board[center] = player2
                else:
                    # try catch a side
                    block = computerTurnLogic(player2, sides)


def computerTurnLogic(symbol, board_list):
    the_block = random.choice(board_list)
    if board[the_block] != '':
        board_list.remove(the_block)
        the_block = -1
    else:
        board[the_block] = symbol
    # while a block was not chosen and the list is not empty
    while the_block == -1 and len(board_list) != 0:
        # get random element from the list
        the_block = random.choice(board_list)
        if board[the_block] != '':
            # remove element from list if it is not empty (cannot choose it)
            board_list.remove(the_block)
            # keep searching
            the_block = -1
        else:
            # put symbol on that place
            board[the_block] = symbol
    # return chosen block number, or -1
    return the_block


def checkIfPlayerWinsNextTurn(symbol):
    copy_board = board.copy()
    # for each empty square, check if user can put his symbol and win
    for i in range(9):
        if copy_board[i] == '':
            copy_board[i] = symbol
            # check for 2 symbols in a row where you can add the third
            ans = checkBordForWin(symbol, copy_board)
            copy_board[i] = ''
            if ans:
                # return where to put symbol next turn
                return i
    # cannot win next turn
    return -1


def checkBordForWin(symbol, tmp_board=None):
    if tmp_board is None:
        tmp_board = board
    # check all 8 options for winning, received a symbol to check and return 1 if true 0 if false
    j = 0
    for i in range(3):  # check horizontal
        if tmp_board[j] == symbol and tmp_board[j + 1] == symbol and tmp_board[j + 2] == symbol:
            return True
        j += 3

    j = 0
    for i in range(3):  # check vertical
        if tmp_board[j] == symbol and tmp_board[j + 3] == symbol and tmp_board[j + 6] == symbol:
            return True
        j += 1

    # check left cross
    if tmp_board[0] == symbol and tmp_board[4] == symbol and tmp_board[8] == symbol:
        return True
    # check right cross
    elif tmp_board[2] == symbol and tmp_board[4] == symbol and tmp_board[6] == symbol:
        return True
    return False


def printBoard(surface):
    grid.draw(surface)
    # run over all board items
    for item in enumerate(board):
        # if it's 1 print X
        if item[1] == 1:
            image_show = pygame.image.load('img/X_.jpeg')
            surface.blit(image_show, board_tuples[item[0]])
            pygame.display.update()
        # if it's 0 print O
        elif item[1] == 0:
            image_show = pygame.image.load('img/O_.jpeg')
            surface.blit(image_show, board_tuples[item[0]])
            pygame.display.update()


def printScreen(surface, toPrint):
    color = (100, 255, 120)
    endfont = pygame.font.SysFont("Goudy Old Style", 60, bold=True)
    text_win = endfont.render(toPrint, 1, color)

    surface.blit(text_win, (100, 200))
    pygame.display.update()
    # ask the user if wants to play again
    surface.blit(endfont.render("Play again? (y/ n)", 1, color), (120, 355))
    pygame.display.update()

    # wait for user input
    while True:
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_n):
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                reset(surface)
                startGame(surface)
    # pygame.quit()
    # sys.exit()


def reset(surface):
    global board
    board = ['', '', '',
             '', '', '',
             '', '', '', ]
    grid.draw(surface)


def chooseMode(surface):
    draw_text_middle(surface, "Choose game mode: ", 50, (200, 200, 200), 315, 50)
    # print on screen 2 options
    button1 = Button(120, 200, surface, 180, " 1 player")
    button2 = Button(320, 200, surface, 180, "2 players")
    button1.draw()
    button2.draw()
    pygame.display.flip()


def chooseSymbol(surface):
    draw_text_middle(surface, "Choose your symbol: ", 50, (200, 200, 200), 315, 50)
    # print on screen X and O
    button1 = Button(170, 200, surface, 90, "X")
    button2 = Button(370, 200, surface, 90, "O")
    button1.draw()
    button2.draw()
    pygame.display.flip()


def start():
    # create a surface
    surface = pygame.display.set_mode((600, 600))
    # start the game
    startGame(surface)
