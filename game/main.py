import pygame
import time
from enum import Enum

# set up global variables
display_width = 800
display_height = 600

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# init game and PyGame variables
pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ScorchedEarth')
clock = pygame.time.Clock()


# PyGame fonts
class FontSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

small_font = pygame.font.SysFont("comicsansms", 25)
med_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 85)


def text_object(text, color, size=FontSize.SMALL):
    """
    Returns text field as rectangle object
    :param text: text to be placed
    :param color: color of the text
    :param size: size of the text (small, medium, large)
    :return: text object and borders of text as rectangle
    """
    if size == FontSize.SMALL:
        text_surface = small_font.render(text, True, color)
    elif size == FontSize.MEDIUM:
        text_surface = med_font.render(text, True, color)
    elif size == FontSize.LARGE:
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(text, color, y_displace=0, size=FontSize.SMALL):
    """
    Places text to screen
    :param text: text to place
    :param color: color of the text
    :param y_displace: vertical displacement of the text, positive/negative values
    :param size: size of the text (small, medium, large)
    :return: none
    """
    text_surf, text_rect = text_object(text, color, size)
    text_rect.center = (int((display_width / 2)), int((display_height / 2) + y_displace))
    gameDisplay.blit(text_surf, text_rect)


def game_loop():
    game_exit = False
    game_over = False
    fps = 15

    while not game_exit:

        if game_over:
            message_to_screen("Game over", red, -50, FontSize.LARGE)
            message_to_screen("S - play again, Q - quit", black, 50)
            pygame.display.update()
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_exit = True
                            game_over = False
                        if event.key == pygame.K_s:
                            game_loop()
                    elif event.type == pygame.QUIT:
                        game_exit = True
                        game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # change angle
                    pass
                elif event.key == pygame.K_DOWN:
                    # change angle
                    pass
                elif event.key == pygame.K_LEFT:
                    # move tank left
                    pass
                elif event.key == pygame.K_RIGHT:
                    # move tank right
                    pass

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, black, [300, 400, 10, 100])
        pygame.display.update()
        clock.tick(fps)

game_loop()

message_to_screen("Bye", black, -50, FontSize.LARGE)
pygame.display.update()
time.sleep(2)
pygame.quit()
