import pygame
import time
from enum import Enum
from math import pi, cos, sin

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
tank_width = 40
tank_height = 12
turret_width = 3
turret_length = int(tank_width/2) + 5
wheel_width = 5
move_step = 3
angle_step = pi/32

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


def fire_simple_shell(gun_end_coord, gun_angle, speed=100):
    """
    Show animation of shooting simple shell
    :param gun_end_coord: initial point of shell
    :param gun_angle: initial angle
    :param speed: initial speed
    :return: none
    """
    fire = True

    print(gun_angle)

    shell_position = list(gun_end_coord)
    horizontal_speed = int(speed * sin(gun_angle))
    elapsed_time = 1

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                halt_whole_game()

        pygame.draw.circle(game_display, green, (shell_position[0], shell_position[1]), 5)

        vertical_speed = -(int(speed * cos(gun_angle)) - 10*elapsed_time)
        print(vertical_speed)
        shell_position[0] += horizontal_speed
        shell_position[1] += vertical_speed
        elapsed_time += 1

        if shell_position[1] > display_height:
            fire = False
        if shell_position[0] > display_width or shell_position[0] < 0:
            fire = False

        pygame.display.update()
        clock.tick(15)


def halt_whole_game():
    """
    Halt the whole program
    :return: none
    """
    pygame.quit()
    quit()


def draw_tank(coord_x, coord_y, turret_angle, color):
    """
    Draws a tank on specified coordinates
    :param coord_x: X coordinate of tank center
    :param coord_y: Y coordinate of tank center
    :param turret_angle: angle of tank's turret
    :param color: color of the tank
    :return: current position of turret end as tuple (x,y)
    """
    x = int(coord_x)
    y = int(coord_y)
    pygame.draw.circle(game_display, color,  (x, y), int(tank_height/4*3))
    pygame.draw.rect(game_display, color, (x-int(tank_width/2), y, tank_width, tank_height))

    new_x = x + int(sin(turret_angle) * turret_length)
    new_y = (y-2) - int(cos(turret_angle) * turret_length)
    pygame.draw.line(game_display, color, (x, y-2), (new_x, new_y), turret_width)

    # draw wheels? is it needed??
    pygame.draw.circle(game_display, color, (x - 15, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x - 10, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x - 5, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x + 5, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x + 10, y + tank_height), wheel_width)
    pygame.draw.circle(game_display, color, (x + 15, y + tank_height), wheel_width)

    return new_x, new_y


def update_tank_coordinates(coord_x, move_tank):
    """
    Update coordinates of the tank
    :param coord_x: current X coordinate
    :param move_tank: change of X coordinate
    :return: updated coordinate
    """
    if move_tank > 0:
        return min(coord_x+move_tank, display_width-int(tank_width/2))
    elif move_tank < 0:
        return max(coord_x+move_tank, int(tank_width/2))
    else:
        return coord_x


def update_turret_angle(current_angle, angle_change):
    """
    Update turrent angle
    :param current_angle: current angle of the turret
    :param angle_change: angle change
    :return: updated angle
    """
    if angle_change > 0:
        return min(current_angle+angle_change, pi/2)
    elif angle_change < 0:
        return max(current_angle+angle_change, -pi/2)
    else:
        return current_angle


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

    main_tank_x = display_width * 0.9
    main_tank_y = display_height * 0.9
    main_tank_turret_angle = -pi / 2
    move_tank = 0
    angle_change = 0

    while not game_exit:

        game_display.fill(black)
        gun = draw_tank(main_tank_x, main_tank_y, main_tank_turret_angle, white)

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
                    angle_change = angle_step
                elif event.key == pygame.K_DOWN:
                    # change angle
                    angle_change = -angle_step
                elif event.key == pygame.K_LEFT:
                    # move tank left
                    move_tank = -move_step
                elif event.key == pygame.K_RIGHT:
                    # move tank right
                    move_tank = move_step
                elif event.key == pygame.K_SPACE:
                    fire_simple_shell(gun, main_tank_turret_angle)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    move_tank = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    angle_change = 0

        main_tank_x = update_tank_coordinates(main_tank_x, move_tank)
        main_tank_turret_angle = update_turret_angle(main_tank_turret_angle, angle_change)
        pygame.display.update()
        clock.tick(fps)


# game_intro()
game_loop()

# message_to_screen("Bye", white, -50, FontSize.LARGE)
pygame.display.update()
# time.sleep(2)
halt_whole_game()
