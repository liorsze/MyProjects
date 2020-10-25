import random


class Food:
    def __init__(self, sh, sw):
        # get food coordinations
        self.x = random.randint(2, sw - 1)
        self.y = random.randint(2, sh - 1)
        self.food_place = None

    def createFood(self, snake, box, stdscr):
        # check that food in scope and not on snake body
        temp_food = None
        while temp_food is None:
            temp_food = [random.randint(box[0][0] + 1, box[1][0] - 1),
                         random.randint(box[0][1] + 1, box[1][1] - 1)]
            if temp_food in snake:
                temp_food = None
        # save new data
        self.food_place = temp_food
        self.x = temp_food[0]
        self.y = temp_food[1]
        # put on screen ? as food
        stdscr.addch(self.food_place[0], self.food_place[1], '*')
