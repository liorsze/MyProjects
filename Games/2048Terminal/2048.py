from Board import Board, screen_clear


def playGame():
    print('Welcome to 2048\n'
          'Your goal is to create the number 2048 by sliding the numbers on the grid\n'
          'You can move up, down, right, left.\n'
          'Good Luck!\n')

    play = True

    # continue playing new games
    while play:
        board = Board()
        # call the game to start
        board.game()
        ans = input('\nDo you want to play another round? Y/N\n')
        if ans == 'N' or ans == 'n':
            play = False
    # clean the screen from the board
    screen_clear()


if __name__ == '__main__':
    playGame()
