import pygame
import random
from game_core.constants import *


def halt_whole_game():
    """
    Halt the whole program
    :return: none
    """
    pygame.quit()
    quit()


def animate_explosion(game_display, start_point, size=50):
    """
    Animates custom explosion on screen on specified coordinates
    :param game_display: display to operate with
    :param size: power (radius) of explosion
    :param start_point: (x,y) coordinates of explosion
    :return: none
    """
    clock = pygame.time.Clock()
    explode = True
    color_choices = [white, red, green, blue, nice_color]
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                halt_whole_game()

        magnitude = 1
        while magnitude < size:
            exploding_bit_x = start_point[0] + random.randrange(-1*magnitude, magnitude)
            exploding_bit_y = start_point[1] + random.randrange(-1*magnitude, magnitude)

            pygame.draw.circle(game_display,
                               random.choice(color_choices),
                               (exploding_bit_x, exploding_bit_y),
                               random.randrange(1, 5))
            magnitude += 1
            pygame.display.update()
            clock.tick(100)

        explode = False

