# Import and initialize the pygame library
import math
import random
from time import sleep
from Button import *

# Import and initialize the pygame library
pygame.init()
WIDTH = 800
HEIGHT = 700
RADIUS = 20
GAP = 15
words = ["banana", "apple", "hamburger", "ice-cream", "lemon", "pineapple", "pizza", "kiwi", "cheese",
         "watermelon", "spaghetti", "cat", "cow", "dog", "bird", "tiger", "lion", "scorpion", "elephant", "monkey"]

hangman_arr = []
# load images.
for i in range(9):
    image = pygame.image.load("img/hangman" + str(i + 1) + ".png")
    hangman_arr.append(image)


# from random_word import RandomWords
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    split_words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in split_words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def createButtons():
    letters = []
    start_x = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    start_y = 500
    for count in range(ord('a'), ord('z') + 1):
        j = count - 97
        # get x and y positions
        x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (j % 13))
        y = start_y + ((j // 13) * (GAP + RADIUS * 2))
        # add button to the list
        letters.append(Button(x, y, chr(count)))
    return letters


def drawOnScreen(guessed_letters, random_word, screen, letters, lose, score):
    screen.fill((0, 153, 153))
    win = printDispaly(guessed_letters, random_word, screen)
    drawButtons(letters, screen)
    screen.blit(hangman_arr[lose], (10, 10))

    # print user score at this point
    print_score = "score: " + str(score)
    font = pygame.font.SysFont("Goudy Old Style", 20)
    text = font.render(print_score, 1, (0, 0, 0))
    screen.blit(text, (int(WIDTH / 2), 10))
    pygame.display.update()
    if win:
        return True
    return False


def printDispaly(guessed_letters, random_word, screen):
    display = ""
    # print _ for each letter in the word which wasn't guessed yet
    for letter in random_word:
        if letter in guessed_letters or letter == "-":
            display += letter + " "
        else:
            display += "_ "
    font = pygame.font.SysFont("Goudy Old Style", 45)
    text = font.render(display, 1, (0, 0, 0))
    screen.blit(text, (int(WIDTH / 2), int(HEIGHT / 9)))
    format_display = display.replace(" ", "")
    # guessed the word
    if format_display == random_word:
        return True
    return False


def drawButtons(letters, screen):
    # draw buttons on the screen
    for button in letters:
        button.draw(screen)


def printScreen(screen, score, toPrint, color, end):
    endfont = pygame.font.SysFont("Goudy Old Style", 60)
    text_win = endfont.render(toPrint, 1, color)
    score_str = "Score: " + str(score)

    screen.blit(text_win, (int(WIDTH / 3), int(HEIGHT / 3)))
    text_score = endfont.render(score_str, 1, color)
    screen.blit(text_score, (int(WIDTH / 3), int(HEIGHT / 3) + 60))
    pygame.display.update()
    sleep(1)
    # ask the user if wants to play again
    screen.blit(endfont.render("Play again? (y/ n)", 1, color), (140, 355))
    pygame.display.update()

    run = True
    # wait for user input
    while run:
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_n):
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                # 'y' is pressed to start a new game - play again
                if end == 1:
                    startGame(score + 8)
                elif end == 0:
                    startGame(8)


def startGame(score):
    # Set up the drawing window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # set title and icon
    pygame.display.set_caption("Hangman!")
    icon = pygame.image.load("img/icon.png")
    pygame.display.set_icon(icon)

    # create a text surface object, on which text is drawn on it.
    text = "welcome to HANGMAN!\n" \
           "Your goal is to guess the words and collect points\n" \
           "Good Luck!\n"

    # Fill the background with blue-ish
    screen.fill((255, 229, 204))

    # screen.blit(text, (100, 100))
    myfont = pygame.font.SysFont("Goudy Old Style", 30)
    blit_text(screen, text, (20, 20), myfont)

    image_show = pygame.image.load('img/hangman-game.png')
    screen.blit(image_show, (280, 120))

    pygame.display.update()

    sleep(3)
    # remove text from screen - re-color it
    screen.fill((0, 153, 153))

    # create list of buttons
    letters = createButtons()

    # letters the user already guessed
    guessed_letters = []
    # score = 0
    lose_index = 0
    word = random.choice(words)

    # Run until the user asks to quit
    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # get mouse positions
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION:
                # CHECK IF MOUSE IS ON ANY BUTTONS
                for button in letters:
                    if button.mouseOn(mouse_x, mouse_y):
                        button.color = (160, 160, 160)
                    else:
                        button.color = (153, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in letters:
                    if button.visible:
                        dis = math.sqrt((button.x - mouse_x) ** 2 + (button.y - mouse_y) ** 2)
                        if dis < RADIUS:
                            button.visible = False
                            guessed_letters.append(button.letter)
                            if button.letter not in word:
                                lose_index += 1
                                score -= 1
        # draw letter on the screen
        win = drawOnScreen(guessed_letters, word, screen, letters, lose_index, score)
        # the user won
        if win:
            winner = "You Won!!! :)"
            running = printScreen(screen, score, winner, (204, 0, 102), 1)
        # the user lost
        elif lose_index == len(hangman_arr) - 1:
            loser = "You Lost! :("
            running = printScreen(screen, score, loser, (255, 0, 5), 0)


def start():
    startGame(8)
