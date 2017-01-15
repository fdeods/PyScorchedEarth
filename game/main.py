import pygame
import time
from enum import Enum

# set up global variables
display_width = 800
display_height = 600

# color constants
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# tank constants
main_tank_x = display_width * 0.9
main_tank_y = display_height * 0.9
tank_width = 40
tank_height = 12
turret_width = 3
wheel_width = 5

# init game and PyGame variables
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
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
    game_display.blit(text_surf, text_rect)


def halt_whole_game():
    """
    Halt the whole program
    :return: none
    """
    pygame.quit()
    quit()


def draw_tank(coord_x, coord_y, color):
    x = int(coord_x)
    y = int(coord_y)
    pygame.draw.circle(game_display, color,  (x, y), int(tank_height/4*3))
    pygame.draw.rect(game_display, color, (x-int(tank_width/2), y, tank_width, tank_height))
    pygame.draw.line(game_display, color, (x, y), (x-10, y-20), turret_width)

    # draw wheels? is it needed??
    pygame.draw.circle(game_display, color, (x - 15, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x - 10, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x - 5, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x + 5, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x + 10, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x + 15, y + tank_height), wheel_width)


def game_intro():
    """
    Some kind of menu
    :return: none
    """
    intro = True

    game_display.fill(white)
    message_to_screen("Welcome to Tanks!", green, -100, FontSize.LARGE)
    message_to_screen("Have fun", black, -30)
    message_to_screen("Press S to play, P to pause or Q to quit", black, 180)
    pygame.display.update()

    clock.tick(15)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                halt_whole_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    halt_whole_game()
                elif event.key == pygame.K_s:
                    intro = False


def game_loop():
    game_exit = False
    game_over = False
    fps = 15

    while not game_exit:

        if game_over:
            message_to_screen("Game over", red, -50, FontSize.LARGE)
            message_to_screen("S - play again, Q - quit", green, 50)
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

        game_display.fill(black)
        draw_tank(main_tank_x, main_tank_y, white)
        pygame.display.update()
        clock.tick(fps)


#game_intro()
game_loop()

#message_to_screen("Bye", white, -50, FontSize.LARGE)
pygame.display.update()
#time.sleep(2)
halt_whole_game()
