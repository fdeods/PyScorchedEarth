import pygame
import random
from game_core.constants import *


def sys_text_object(text, color, size=FontSize.SMALL):
    """
    Returns text field as rectangle object
    :param text: text to be placed
    :param color: color of the text
    :param size: size of the text (small, medium, large)
    :return: text object and borders of text as rectangle
    """
    font_string = 'comicsansms'
    if size == FontSize.SMALL:
        text_surface = pygame.font.SysFont(font_string, 25).render(text, True, color)
    elif size == FontSize.MEDIUM:
        text_surface = pygame.font.SysFont(font_string, 50).render(text, True, color)
    elif size == FontSize.LARGE:
        text_surface = pygame.font.SysFont(font_string, 85).render(text, True, color)
    return text_surface, text_surface.get_rect()


def custom_text_object(text, color, size=FontSize.SMALL):
    """
    Returns text field as rectangle object
    :param text: text to be placed
    :param color: color of the text
    :param size: size of the text (small, medium, large)
    :return: text object and borders of text as rectangle
    """
    font_string = 'assets/fonts/font.ttf'
    if size == FontSize.SMALL:
        text_surface = pygame.font.Font(font_string, 25).render(text, True, color)
    elif size == FontSize.MEDIUM:
        text_surface = pygame.font.Font(font_string, 50).render(text, True, color)
    elif size == FontSize.LARGE:
        text_surface = pygame.font.Font(font_string, 85).render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(game_display, text, color, y_displace=0, size=FontSize.SMALL, sys_font=True):
    """
    Places text to screen
    :param game_display: handle to display
    :param text: text to place
    :param color: color of the text
    :param y_displace: vertical displacement of the text, positive/negative values
    :param size: size of the text (small, medium, large)
    :return: none
    """
    if sys_font:
        text_surf, text_rect = sys_text_object(text, color, size)
    else:
        text_surf, text_rect = custom_text_object(text, color, size)
    text_rect.center = (int((display_width / 2)), int((display_height / 2) + y_displace))
    game_display.blit(text_surf, text_rect)


def halt_whole_game():
    """
    Halt the whole program
    :return: none
    """
    pygame.quit()
    quit()


def animate_explosion(game_display, start_point, sound, size=50):
    """
    Animates custom explosion on screen on specified coordinates
    :param game_display: display to operate with
    :param size: power (radius) of explosion
    :param start_point: (x,y) coordinates of explosion
    :param sound: sound of explosion
    :return: none
    """
    clock = pygame.time.Clock()
    pygame.mixer.Sound.play(sound)
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


def animate_ground_sloughing(game_display, left_ground, ground):
    """
    Animates ground sloughing
    :param game_display: display to operate with
    :param left_ground: list of all ground pieces to slough
    :param ground: Ground object
    :return: none
    """
    clock = pygame.time.Clock()
    normalized = 0
    while normalized < len(left_ground):
        normalized = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                halt_whole_game()

        for line in left_ground:
            pygame.draw.line(game_display,
                             black,
                             line[0],
                             line[1])
            if line[0][1] == ground.get_ground_height_at_point(line[0][0]):
                normalized += 1
            else:
                line[0][1] += 1
                line[1][1] += 1
            pygame.draw.line(game_display,
                             dark_green,
                             line[0],
                             line[1])

        pygame.display.update()
        clock.tick(100)
