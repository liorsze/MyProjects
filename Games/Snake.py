import curses
import random


class Snake:
    def __init__(self, sh, sw):
        # coordinations to begin at
        self.x = random.randint(2, sw - 1)
        self.y = random.randint(2, sh - 1)
        # create a snake
        self.snake_body = [[self.y, self.x], [self.y, self.x-1]]

    def putOnScreen(self, stdscr):
        # print on screen # as body
        for s, t in self.snake_body:
            stdscr.addstr(s, t, '#')

    def move(self, key):
        # get the head of the snake
        head = self.snake_body[0]
        # check snake direction and return it
        if key == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
            return new_head
        elif key == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
            return new_head
        elif key == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]
            return new_head
        elif key == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
            return new_head
