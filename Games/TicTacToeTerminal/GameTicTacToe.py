import os
import random

from time import sleep


# The screen clear function
def screen_clear():
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')


board = ['_', '_', '_',
         '_', '_', '_',
         '_', '_', '_', ]
boardtumplet = ['1', '2', '3',
                '4', '5', '6',
                '7', '8', '9', ]

player1 = -1
player2 = -1
activePlayer = -1
gamemode = -1


def printboard():
    global board, boardtumplet
    j = 0

    # for i in range(3):
    #     print(" ___" * 3 + "\t\t" + " ___" * 3)
    #     print("|\t" * 4 + "\t" + "|\t" * 4)
    #     print(" _" + str(board[j]) + "_" + " _" + str(board[j + 1]) + "_" + " _" + str(
    #         board[j + 2]) + "_" + "\t\t" + " _" +
    #           str(boardtumplet[j]) + "_" + " _" + str(boardtumplet[j + 1]) + "_" + " _" + str(
    #         boardtumplet[j + 2]) + "_")
    #     j += 3
    #

    global board, boardtumplet
    for i in range(3):
     print(("|" + "\u203e" * 3 + "|") * 3 + "\t\t" + ("|" + "\u203e" * 3 + "|") * 3)
     print("|" + "_" + board[j] + "_" + "|" + "|" + "_" + board[j + 1] + "_" + "|" + "|" + "_" + board[
         j + 2] + "_" + "|\t\t" + "|" + "_" + boardtumplet[j] + "_" + "|" + "|" + "_" + boardtumplet[
               j + 1] + "_" + "|" + "|" + "_" + boardtumplet[
               j + 2] + "_" + "|")
     j += 3


def start():
    screen_clear()
    global player1, player2, activePlayer, gamemode

    print("Welcome to TIC TAC TOE!\n"
          "Please select game mode:\n"
          "For 2 players select 2\n"
          "For 1 player vs computer select 1")
    gamemode = int(input())
    if gamemode != 1 and gamemode != 2:
        gamemode = -1

    while gamemode == -1:
        print("Wrong input!\n"
              "Please select game mode:\n"
              "For 2 players select 2\n"
              "For 1 player vs computer select 1")
        gamemode = int(input())
        if gamemode != 1 and gamemode != 2:
            gamemode = -1
    if gamemode == 2:
        twoplayersgamemode()
    else:
        oneplayergamemode()


def twoplayersgamemode():  # this is 2 players game mode
    global player1, player2, activePlayer, gamemode, board

    print("Player 1 please choose X or O")
    print("Press 1 for X or 0 for O")
    inputSymbol = int(input())
    if inputSymbol == 1:
        player1 = 'X'
        player2 = 'O'
    elif inputSymbol == 0:
        player1 = 'O'
        player2 = 'X'
    while player1 == -1:
        print("Wrong input!")
        print("Player 1 please choose X or O")
        print("Press 1 for X or 0 for O")
        inputSymbol = int(input())
        if inputSymbol == 1:
            player1 = 'X'
            player2 = 'O'
        elif inputSymbol == 0:
            player1 = 'O'
            player2 = 'X'
    if player1 == 'X':
        screen_clear()
        print("Player 1 is X\n"
              "Player 2 is O")
    else:
        screen_clear()
        print("Player 1 is O\n"
              "Player 2 is X")
    win = -1
    for i in range(9):
        if i % 2 == 0:
            print("Player1 turn")
            turn(player1)
            screen_clear()
            win = checkbordforwin(player1, board)
            if win == 1:
                printboard()
                print("player1 has won!!!\n")

                break
        else:
            print("Player2 turn")
            turn(player2)
            screen_clear()
            win = checkbordforwin(player2, board)
            if win == 1:
                printboard()
                print("player2 has won!!!\n")
                break
    if win == -1:
        printboard()
        print("Its a tie!!")
    print("Do you want to play again? Y/N ")
    ans = input().upper()
    if ans == 'Y':
        resetgame()
    else:
        quitgame()


def oneplayergamemode():
    global player1, player2, activePlayer, gamemode, board
    print("Player 1 please choose X or O")
    print("Press 1 for X or 0 for O")
    inputSymbol = int(input())
    if inputSymbol == 1:
        player1 = 'X'
        player2 = 'O'
    elif inputSymbol == 0:
        player1 = 'O'
        player2 = 'X'
    while player1 == -1:
        print("Wrong input!")
        print("Player 1 please choose X or O")
        print("Press 1 for X or 0 for O")
        inputSymbol = int(input())
        if inputSymbol == 1:
            player1 = 'X'
            player2 = 'O'
        elif inputSymbol == 0:
            player1 = 'O'
            player2 = 'X'
    screen_clear()
    print("Your are " + player1)
    print("Computer is " + player2)
    win = -1
    for i in range(9):
        if i % 2 == 0:
            turn(player1)
            screen_clear()
            win = checkbordforwin(player1, board)
            if win == 1:
                printboard()
                print("You have won!!!\n")
                break
        else:
            print("Computer turn.")
            sleep(0.5)
            screen_clear()
            printboard()
            print("Computer turn..")
            sleep(0.5)
            screen_clear()
            printboard()
            print("Computer turn...")
            sleep(0.5)
            screen_clear()
            printboard()
            print("Computer turn.")
            sleep(0.5)
            screen_clear()
            printboard()
            print("Computer turn..")
            sleep(0.5)
            screen_clear()
            cpturn(player2)
            win = checkbordforwin(player2, board)
            if win == 1:
                printboard()
                print("You lose..")
                break
    if win == -1:
        printboard()
        print("Its a tie!!")
    print("Do you want to play again? Y/N ")
    ans = input().upper()
    if ans == 'Y':
        resetgame()
    else:
        quitgame()


def checkbordforwin(
        symbol, b):  # check all 8 options for winning, recived a symbol to check and return 1 if true 0 if false
    global player1, player2, activePlayer, gamemode
    j = 0
    for i in range(3):  # check horizontal
        if b[j] == symbol and b[j + 1] == symbol and b[j + 2] == symbol:
            return 1
        j += 3

    j = 0
    for i in range(3):  # check vertical
        if b[j] == symbol and b[j + 3] == symbol and b[j + 6] == symbol:
            return 1
        j += 1

    # check left cross
    if b[0] == symbol and b[4] == symbol and b[8] == symbol:
        return 1
    # check right cross
    elif b[2] == symbol and b[4] == symbol and b[6] == symbol:
        return 1
    return -1


def turn(symbol):

    inputblock = -1
    printboard()
    print("Choose a block (1-9) :")
    inputblock = int(input())
    if inputblock < 1 or inputblock > 9:
        inputblock = -1
        print("Block not in range!")
    if board[inputblock - 1] != '_':
        inputblock = -1
        print("Block already used!1")

    while inputblock == -1:
        print("Choose a block (1-9) :")
        inputblock = int(input())
        if inputblock < 1 or inputblock > 9:
            inputblock = -1
            print("Block not in range!")
        if board[inputblock - 1] != '_':
            inputblock = -1
            print("Block already used!2")
    board[inputblock - 1] = symbol


def cpturn(symbol):
    global player1, player2, activePlayer, gamemode
    corners = [0, 2, 6, 8]
    sides = [1, 3, 5, 7]
    # fisrt check if cp win next turn
    block = -1
    block = checkifplayerwinsnextturn(symbol)
    if block != -1:
        board[block] = symbol
    else:
        # check if player win next turn and block him
        block = checkifplayerwinsnextturn(player1)
        if block != -1:
            board[block] = symbol
        else:
            # try to catch a corner
            block = random.choice(corners)
            if board[block] != '_':
                corners.remove(block)
                block = -1
            else:
                board[block] = symbol
            while block == -1 and len(corners) != 0:
                block = random.choice(corners)
                if board[block] != '_':
                    corners.remove(block)
                    block = -1
                else:
                    board[block] = symbol
            if block == -1:
                # try center
                if board[4] == '_':
                    board[4] = symbol
                else:
                    # try catch a side
                    block = random.choice(sides)
                    if board[block] != '_':
                        sides.remove(block)
                        block = -1
                    else:
                        board[block] = symbol
                    while block != -1:
                        block = random.choice(sides)
                        if board[block] != '_':
                            corners.remove(block)
                            block = -1
                        else:
                            board[block] = symbol


def checkifplayerwinsnextturn(symbol):
    global player1, player2, activePlayer, gamemode, board
    copyboard = board.copy()
    ans = -1
    for i in range(9):
        if copyboard[i] == '_':
            copyboard[i] = symbol
            ans = checkbordforwin(symbol, copyboard)
            copyboard[i] = '_'
        if ans != -1:
            return i
    return ans


def resetgame():
    global player1, player2, activePlayer, gamemode, board
    board = ['_', '_', '_',
             '_', '_', '_',
             '_', '_', '_', ]
    player1 = -1
    player2 = -1
    gamemode = -1
    start()


def quitgame():
    print("Thank you for playing TIC TAC TOE")
