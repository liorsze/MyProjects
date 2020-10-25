import pygame
# from HangmanMain import RADIUS, GAP
RADIUS = 20
GAP = 15


class Button(object):

    def __init__(self, x, y, letter=''):
        self.visible = True
        # self.rollOver = False
        self.x = x
        self.y = y
        self.color = (153, 255, 255)
        self.letter = letter

    def draw(self, screen):
        if self.visible:
            pygame.draw.circle(screen, self.color, (self.x, self.y), RADIUS, 0)
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), RADIUS, 2)
            thefont = pygame.font.SysFont('Goudy Old Style', 30)
            text = thefont.render(self.letter, 1, (0, 0, 0))
            screen.blit(text, (int(self.x - text.get_width() / 2), int(self.y - text.get_height() / 2)))
        else:
            pygame.draw.circle(screen, (0, 153, 153), (self.x, self.y), RADIUS, 0)
            pygame.draw.circle(screen, (0, 153, 153), (self.x, self.y), RADIUS, 2)

    def mouseOn(self, mouse_x, mouse_y):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < mouse_x < self.x + RADIUS*2 + GAP:
            if self.y < mouse_y < self.y + RADIUS*2 + GAP:
                return True
        return False
