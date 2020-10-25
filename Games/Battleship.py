from time import sleep

from termcolor import colored
from GameTicTacToe import screen_clear

import copy
import random
import Ship

w, h = 9, 9
boardplayer1 = [['_' for x in range(w)] for y in range(h)]
boardplayer2 = [['_' for x in range(w)] for y in range(h)]
fleet1 = []
fleet2 = []
boardhitsplayer1 = []
boardhitsplayer2 = []
memrow, memcol, usemem = -1, -1, False


def initboard():
    global boardplayer1, boardplayer2, boardhitsplayer1, boardhitsplayer2
    boardplayer1[0][0] = '_'
    boardplayer2[0][0] = '_'
    for i in range(8):
        boardplayer1[0][i + 1] = colored(chr(ord('A') + i), 'yellow')
        boardplayer1[i + 1][0] = colored(i + 1, 'yellow')
        boardplayer2[0][i + 1] = colored(chr(ord('A') + i), 'yellow')
        boardplayer2[i + 1][0] = colored(i + 1, 'yellow')
    boardhitsplayer1 = copy.deepcopy(boardplayer1)
    boardhitsplayer2 = copy.deepcopy(boardplayer2)


def printboard(board):
    j = 0
    for i in range(9):
        print(("|" + "\u203e" * 3 + "|") * 9)  # + "\t\t" + ("|" + "\u203e" * 3 + "|") * 3)
        print("|" + "_" + str(board[i][j]) + "_" + "|" + "|" + "_" + str(
            board[i][j + 1]) + "_" + "|" + "|" + "_" + str(board[i][j + 2]) + "_" + "|" + "|" + "_" + str(
            board[i][j + 3]) + "_" + "|" + "|" + "_" + str(board[i][j + 4]) + "_" + "|" + "|" + "_" + str(
            board[i][j + 5]) + "_" + "|" + "|" + "_" + str(board[i][j + 6]) + "_" + "|" + "|" + "_" + str(
            board[i][j + 7]) + "_" + "|" + "|" + "_" + str(board[i][j + 8]) + "_" + "|")


def startgame():
    screen_clear()
    global fleet1, fleet2, boardhitsplayer2, boardplayer1, boardplayer2, boardhitsplayer1
    initboard()
    win = False
    print("\nWelcome to BattleShip.\n")
    print("\nThis is your fleet:")
    print("##\t##\t###\t###\t#####\n\n")
    print("Your opponent has the same fleet,\nthe goal is to sink all of the opponent's ships.")
    print("\nGood luck!!")
    makefleet()
    placeboats()
    compuderplacefleet()
    print("\nAll set up. Starting the game")
    # players turn
    printboard(boardplayer1)
    sleep(5)
    while not win:
        turn(boardplayer2, boardhitsplayer2, fleet2)
        if checkforwin(fleet2):
            win = True
            printboatstatus(fleet2, boardhitsplayer2)
            printboard(boardhitsplayer2)
            print("You win!!")
        else:
            cpturn(boardplayer1, boardhitsplayer1, fleet1)
        if checkforwin(fleet1):
            win = True
            printboatstatus(fleet1, boardhitsplayer1)
            printboard(boardhitsplayer1)
            print("you loose...")
    print("\nDo you want to play again? Y/N")
    ans = input().upper()
    if ans == 'N':
        endgame()
    else:
        resetgame()


def resetgame():
    global fleet1, fleet2, boardhitsplayer2, boardplayer1, boardplayer2, boardhitsplayer1
    w, h = 9, 9
    boardplayer1 = [['_' for x in range(w)] for y in range(h)]
    boardplayer2 = [['_' for x in range(w)] for y in range(h)]
    fleet1 = []
    fleet2 = []
    boardhitsplayer1 = []
    boardhitsplayer2 = []


def cpturn(board, boardhits, fleet):  # this is the case no hit detected- choose a random location on the board
    print("It's the computers turn")
    global memrow, memcol, usemem
    ok, hit = False, False  # I will use hit to indicate if there is a part sunk ship from last turn
    while not ok or hit:
        row = random.randrange(1, 9)
        col = random.randrange(1, 9)
        if boardhits[row][col] != '_':
            ok = False
        elif usemem:
            ok=True
            usemem = False  # reset usemem
            hit = smartcpturn(board, boardhits, fleet, memrow, memcol)
            if hit and checkforwin(fleet):
                hit = False  # end game
            elif not hit:
                usemem = True  # mark that cp missed this turn but next turn cp need to use mem vars

            # else hit=True and game not finished go to while loop
        else:
            ok = True
            if board[row][col] == colored("#", 'green'):
                boardhits[row][col] = colored("X", 'red')
                printboard(boardhits)
                print("Its a hit!")
                sleep(5)
                checkboatsink(fleet, board, boardhits)
                if not checkforwin(fleet):
                    # if its a hit remember the hit point in case of next turn miss
                    memrow, memcol = row, col
                    # go to smart turn
                    hit = smartcpturn(board, boardhits, fleet, row,col)  # random hits and now do smart if hit=True
                                                                            # ship sank hit=False ship not
                                                                             # sank but cp missed
                    if hit and checkforwin(fleet):
                        hit = False  # end game
                    elif not hit:
                        usemem = True  # mark that cp missed this turn but next turn cp need to use mem vars

                    # else hit=True and game not finished go to while loop

            else:
                boardhits[row][col] = colored("*", 'blue')
                printboard(boardhits)
                print("Missed...")
                hit = False
                sleep(5)


def smartcpturn(board, boardhits, fleet, row, col):
    global memrow, memcol
    temprow, tempcol = row, col  # local vars for row and col
    ok, endsmart = False, False
    list = [1, 2, 3, 4]
    while not ok:
        case = random.choice(list)  # choos a diraction
        if case == 1 and checkvalid(temprow + 1, tempcol, boardhits):
            if board[temprow + 1][tempcol] == colored("#", 'green'):
                boardhits[temprow + 1][tempcol] = colored("X", 'red')
                printboard(boardhits)
                print("It's a hit!")
                sleep(2)
                temprow += 1
                list = [1, 2, 3, 4]  # reset list
                if checkboatsink(fleet, board, boardhits):
                    return True

            else:
                boardhits[temprow + 1][tempcol] = colored("*", 'blue')
                printboard(boardhits)
                print("Missed...")
                sleep(2)
                ok = True  # end of computer turn
        elif case == 2 and checkvalid(row - 1, col, boardhits):
            if board[temprow - 1][tempcol] == colored("#", 'green'):
                boardhits[temprow - 1][tempcol] = colored("X", 'red')
                temprow -= 1
                list = [1, 2, 3, 4]  # reset list
                if checkboatsink(fleet, board, boardhits):
                    return True

            else:
                boardhits[temprow - 1][tempcol] = colored("*", 'blue')
                printboard(boardhits)
                print("Missed...")
                sleep(2)
                ok = True  # end of computer turn
        elif case == 3 and checkvalid(row, col + 1, boardhits):
            if board[temprow][tempcol + 1] == colored("#", 'green'):
                boardhits[temprow][tempcol + 1] = colored("X", 'red')
                printboard(boardhits)
                print("It's a hit!")
                sleep(2)
                tempcol += 1
                list = [1, 2, 3, 4]  # reset list
                if checkboatsink(fleet, board, boardhits):
                    return True

            else:
                boardhits[temprow][tempcol + 1] = colored("*", 'blue')
                printboard(boardhits)
                print("Missed...")
                sleep(2)
                ok = True  # end of computer turn
        elif case == 4 and checkvalid(row, col - 1, boardhits):
            if board[temprow][tempcol - 1] == colored("#", 'green'):
                boardhits[temprow][tempcol - 1] = colored("X", 'red')
                printboard(boardhits)
                print("It's a hit!")
                sleep(2)
                tempcol -= 1
                list = [1, 2, 3, 4]  # reset list
                if checkboatsink(fleet, board, boardhits):
                    return True

            else:
                boardhits[temprow][tempcol - 1] = colored("*", 'blue')
                printboard(boardhits)
                print("Missed...")
                sleep(2)
                ok = True  # end of computer turn
        else:  # case not valid
            list.remove(case)
    return False  # means that there is a part sank ship but this turn missed...


def checkvalid(row, col, boardhits):
    if 0 < row < 9 and 0 < col < 9 and boardhits[row][col] == '_':
        return True
    return False


def turn(board, boardhits, fleet):
    print("its your turn!")
    ok = False
    while not ok or hit:
        hit = False
        printboatstatus(fleet, boardhits)
        printboard(boardhits)

        print("Choose a column (A-H):")
        col = ord(input().upper()) - 64
        while col < 1 or col > 8:
            print("Wrong input!\n")
            print("Choose a column (A-H)")
            col = ord(input()) - 64
        print("Choose a row (1-8):")
        row = int(input())
        while row < 1 or row > 8:
            print("Wrong input!\n")
            print("Choose a row (1-8):")
            row = input()
        if boardhits[row][col] != '_':
            ok = False
            print("Target already marked! Choose another target")
            sleep(2)
        else:
            boardhits[row][col] = colored("O", "green")
            printboard(boardhits)
            print("Target locked!\tReady to fire? Y/N")
            ans = input().upper()
            if ans == 'Y':
                ok = True
                print("Missile launched")
                if board[row][col] == colored("#", 'green'):
                    boardhits[row][col] = colored("X", 'red')
                    print("Its a hit!")
                    checkboatsink(fleet, board, boardhits)
                    if not checkforwin(fleet):
                        hit = True
                else:

                    boardhits[row][col] = colored("*", 'blue')
                    printboard(boardhits)
                    print("Missed...")
                    sleep(3)


def checkboatsink(fleet, board, boardhits):
    mark = False
    for s in fleet:
        row = s.get_number()
        col = s.get_letter()
        size = s.get_size()
        side = s.get_side()
        sink = s.is_sink()
        stop = False
        for i in range(size):
            if sink or stop:
                break
            elif side == 'V':
                if board[row + i][col] == colored('#', 'green') and boardhits[row + i][col] != colored('X', 'red'):
                    stop = True
            else:
                if board[row][col + i] == colored('#', 'green') and boardhits[row][col + i] != colored('X', 'red'):
                    stop = True
        if not stop:
            s.set_sink()
            markbordersinboradhits(boardhits, side, row, col, size)
            mark = True
    return mark


def markbordersinboradhits(boardhits, side, row, col, size):
    if side == 'V':
        for r in range(row,row+size):
            markshipbordersVertical(boardhits, r, col)
        markshipbordertopandbottom(boardhits, row, col, size)
    else:
        for c in range(col,col+size):
            markshipbordersHorizontal(boardhits, row, c)
        markshipborderleftandright(boardhits, row, col, size)


def checkforwin(fleet):
    sink = 0
    for s in fleet:
        if s.is_sink():
            sink += 1
    if sink == 5:
        return True
    return False


def printboatstatus(fleet, board):
    nsink, sink = "", ""
    for s in fleet:
        col = s.get_letter()
        row = s.get_number()
        side = s.get_side()
        size = s.get_size()
        if s.is_sink():
            sink = sink + colored("#", 'red') * s.get_size() + "\t\t"
        else:
            for i in range(s.get_size()):
                if side == 'H':
                    if board[row][col + i] == colored("X", 'red'):
                        nsink = nsink + colored("#", 'red')
                    else:
                        nsink = nsink + "#"
                elif side == 'V':
                    if board[row + i][col] == colored('X', 'red'):
                        nsink = nsink + colored("#", 'red')
                    else:
                        nsink = nsink + "#"
        nsink = nsink + "\t\t"
    print("\t" * 20 + "sank: " + sink)
    print("\t" * 20 + "not sank: " + nsink)


def placeboats():
    global boardplayer1, boardplayer2

    for s in fleet1:
        fail, done = False, False
        while fail or not done:
            fail = False
            printboard(boardplayer1)
            # choose direction
            print(
                "Place this ship:" + "#" * s.get_size() + "\n\nPress V for vertical or H for horizontal.\nHorizontal will "
                                                          "be placed from left to right, vertical will be placed from "
                                                          "up "
                                                          "to down")
            side = input().upper()
            while side != 'V' and side != 'H':
                printboard(boardplayer1)
                print(
                    "Wrong input! \nPlace this ship:" + "#" * s.get_size() + "\n\nPress V for vertical or H for "
                                                                             "horizontal.\nHorizontal will be placed "
                                                                             "from "
                                                                             " left to right, vertical will be placed "
                                                                             "from up to down")
                side = input().upper()
            # choose start point
            # col
            print("Place this ship:" + "#" * s.get_size() + "\n\nEnter a column letter (A-H):")
            col = input().upper()
            while ord(col) < 65 or ord(col) > 72:
                printboard(boardplayer1)
                print(
                    "Wrong input! \nPlace this ship:" + "#" * s.get_size() + "\n\nEnter a column letter (A-H):")
                col = input().upper()
            col = ord(col) - 64  # convert letter to num in range (1-8)
            # row
            print("Place this ship:" + "#" * s.get_size() + "\n\nEnter a row number (1-8):")
            row = int(input())
            while row < 1 or row > 8:
                printboard(boardplayer1)
                print(
                    "Wrong input! \nPlace this ship:" + "#" * s.get_size() + "\n\nEnter a row number (1-8):")
                row = input()

            # check if there is space for ship
            tempboard = copy.deepcopy(boardplayer1)
            if side == 'V':
                for r in range(row, row + s.get_size()):
                    if fail:

                        break
                    elif r > 8 or tempboard[r][col] != '_':
                        print("The ship doesnt have space in this location\n")
                        sleep(4)
                        fail = True
                    else:
                        tempboard[r][col] = colored('#', 'green')
                        markshipbordersVertical(tempboard, r, col)

                if not fail:
                    markshipbordertopandbottom(tempboard, row, col, s.get_size())  # mark top and bottom border
                    boardplayer1 = copy.deepcopy(tempboard)
                    print("Ship is placed!")
                    done = True
                    s.place(col, row, side)
                    sleep(1.05)
            elif side == 'H':
                for c in range(col, col + s.get_size()):
                    if fail:
                        break
                    elif c > 8 or tempboard[row][c] != '_':
                        print("The ship doesnt have space in this location\n")
                        sleep(4)
                        fail = True
                    else:
                        tempboard[row][c] = colored('#', 'green')
                        markshipbordersHorizontal(tempboard, row, c)

                if not fail:
                    markshipborderleftandright(tempboard, row, col, s.get_size())  # mark top and bottom border
                    boardplayer1 = copy.deepcopy(tempboard)
                    print("Ship is placed!")
                    done = True
                    s.place(col, row, side)
                    sleep(1.05)


def markshipbordersVertical(board, row, col):  # thia fun mark left and right borders
    if 1 < col < 8:
        board[row][col - 1] = colored('*', 'blue')
        board[row][col + 1] = colored('*', 'blue')
    elif col == 1:
        board[row][col + 1] = colored('*', 'blue')
    elif col == 8:
        board[row][col - 1] = colored('*', 'blue')


def markshipbordertopandbottom(board, row, col, size):
    if row != 1:
        board[row - 1][col] = colored('*', 'blue')
    if row + size < 9:
        board[row + size][col] = colored('*', 'blue')


def markshipbordersHorizontal(board, row, col):  # mark up and down borders
    if 1 < row < 8:
        board[row + 1][col] = colored('*', 'blue')
        board[row - 1][col] = colored('*', 'blue')
    elif row == 1:
        board[row + 1][col] = colored('*', 'blue')
    elif row == 8:
        board[row - 1][col] = colored('*', 'blue')


def markshipborderleftandright(board, row, col, size):
    if col != 1:
        board[row][col - 1] = colored('*', 'blue')
    if col + size < 9:
        board[row][col + size] = colored('*', 'blue')


def compuderplacefleet():
    global boardplayer2, boardhitsplayer2, fleet2

    for s in fleet2:
        done, fail = False, False

        while fail or not done:
            fail = False
            tempboard = copy.deepcopy(boardplayer2)
            side = random.random()  # return a  float num between 0 to 1
            col = random.randrange(1, 9)
            row = random.randrange(1, 9)
            if side < 0.5:  # horozontal
                side = 'H'
                for c in range(col, col + s.get_size()):
                    if fail:
                        break
                    elif c > 8 or tempboard[row][c] != '_':
                        fail = True
                    else:
                        tempboard[row][c] = colored('#', 'green')
                        markshipbordersHorizontal(tempboard, row, c)
                if not fail:
                    markshipborderleftandright(tempboard, row, col, s.get_size())  # mark top and bottom border
                    boardplayer2 = copy.deepcopy(tempboard)
                    done = True
                    s.place(col, row, side)
            else:
                side = 'V'
                for r in range(row, row + s.get_size()):
                    if fail:
                        break
                    elif r > 8 or tempboard[r][col] != '_':
                        fail = True
                    else:
                        tempboard[r][col] = colored('#', 'green')
                        markshipbordersVertical(tempboard, r, col)

                if not fail:
                    markshipbordertopandbottom(tempboard, row, col, s.get_size())  # mark top and bottom border
                    boardplayer2 = copy.deepcopy(tempboard)
                    done = True
                    s.place(col, row, side)


def makefleet():
    global fleet1, fleet2
    fleet1.append(Ship.Ship(2, 1))
    fleet1.append(Ship.Ship(2, 2))
    fleet1.append(Ship.Ship(3, 3))
    fleet1.append(Ship.Ship(3, 4))
    fleet1.append(Ship.Ship(5, 5))

    fleet2.append(Ship.Ship(2, 1))
    fleet2.append(Ship.Ship(2, 2))
    fleet2.append(Ship.Ship(3, 3))
    fleet2.append(Ship.Ship(3, 4))
    fleet2.append(Ship.Ship(5, 5))


def endgame():
    print("Thank you for playing BattleShips!\nHope to see you again")
