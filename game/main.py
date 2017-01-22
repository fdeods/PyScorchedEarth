import pygame
import random
from enum import Enum
from math import pi, cos, sin, sqrt
from shapely.geometry import LineString

# set up global variables
display_width = 1600
display_height = 900

# color constants
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
good_health_color = green
normal_health_color = (0xff, 0x91, 0x00)
low_health_color = red
blue = (0, 0, 255)
nice_color = (0xfd, 0x30, 0xd5)
dark_green = (0x13, 0x70, 0x2c)

# tank constants
tank_width = 40
tank_height = 12
turret_width = 3
turret_length = int(tank_width/2) + 5
wheel_width = 5
move_step = 3
angle_step = pi/64

# shell constants
min_shell_speed = 10
max_shell_speed = 20
shell_speed_step = (max_shell_speed-min_shell_speed)/100

# init game and PyGame variables
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ScorchedEarth')
clock = pygame.time.Clock()

# temporary simple ground
ground_height = 73

# temporary enemy tank coordinates
e_tank_x = int(display_height * 0.1)
e_tank_y = int(display_height * 0.9)
e_turret_angle = pi/4
e_tank_health = 100


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


def animate_explosion(start_point, size=50):
    """
    Animates custom explosion on screen on specified coordinates
    :param size: power (radius) of explosion
    :param start_point: (x,y) coordinates of explosion
    :return: none
    """
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


def check_collision_with_tank(shell_line):
    """
    Checks whether there was a collision with tank and returns collision coordinates
    :param shell_line: trajectory line of the shell
    :return: intersection point coordinates or None
    """
    return None


def check_collision(prev_shell_position, current_shell_position):
    """
    Checks collision of shell with other objects and return coordinates of shell collision
    :param prev_shell_position: Coordinates of previous shell position
    :param current_shell_position: Coordinates of updated shell position
    :return: Coordinates of collision or None if no collision detected
    """
    line1 = LineString([prev_shell_position, current_shell_position])
    line2 = LineString([[0, display_height-ground_height], [display_width, display_height-ground_height]])

    # temporary check if we hit enemy tank
    # intersection = check_collision_with_tank(line1)
    # if intersection:
    #    return int(intersection.x), int(intersection.y)

    intersection = line1.intersection(line2)

    if intersection:
        return int(intersection.x), int(intersection.y)
    return None


def calculate_distance_from_tank_center(explosion_point):
    """
    Calculates distance from explosion_point to tank center
    :param explosion_point: coordinates of explosion point as tuple
    :return: distance to tank center
    """
    return int(sqrt((explosion_point[0]-e_tank_x)**2+(explosion_point[1]-e_tank_y)**2))


def apply_damage(explosion_point, explosion_power):
    """
    Applies damage taken by tank regarding to position of explosion point and its power
    :param explosion_point: coordinates of explosion point
    :param explosion_power: power of explosion
    :return: none
    """
    global e_tank_health
    distance_from_tank = calculate_distance_from_tank_center(explosion_point)
    print(distance_from_tank)
    damage = 0
    if distance_from_tank < explosion_power:
        damage = int(((explosion_power-distance_from_tank) / explosion_power) * 50)

    print(damage)

    e_tank_health = max(e_tank_health-damage, 0)


def fire_simple_shell(gun_end_coord, gun_angle, power=50):
    """
    Show animation of shooting simple shell
    :param gun_end_coord: initial point of shell
    :param gun_angle: initial angle
    :param power: initial power of shot
    :return: none
    """
    speed = min_shell_speed+shell_speed_step*power
    shell_position = list(gun_end_coord)
    elapsed_time = 0.1

    fire = True

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                halt_whole_game()

        prev_shell_position = list(shell_position)
        vertical_speed = -(int(speed * cos(gun_angle)) - 10 * elapsed_time/2)
        horizontal_speed = int(speed * sin(gun_angle))
        shell_position[0] += int(horizontal_speed*elapsed_time)
        shell_position[1] += int(vertical_speed*elapsed_time)
        elapsed_time += 0.1

        if shell_position[1] > display_height:
            break

        collision_point = check_collision(prev_shell_position, shell_position)

        if collision_point:
            animate_explosion(collision_point)
            apply_damage(collision_point, power)
            fire = False
        else:
            pygame.draw.circle(game_display, red, (shell_position[0], shell_position[1]), 5)

        pygame.display.update()
        clock.tick(60)


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
    Update turret angle
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


def update_tank_power(current_power, power_change):
    """
    Update tank's power
    :param current_power: current tank's power
    :param power_change: change of power
    :return: updated power
    """
    if power_change > 0:
        return min(current_power+power_change, 100)
    elif power_change < 0:
        return max(current_power+power_change, 0)
    else:
        return current_power


def show_tanks_power(current_power):
    """
    Displays tank's power to screen
    :param current_power: power to display
    :return: none
    """
    (text_surface, rect_size) = text_object("Power: "+str(current_power)+"%", white, FontSize.SMALL)
    game_display.blit(text_surface, [int(display_width/2)-int(rect_size.width/2), 10])


def draw_health_bar(health_value, pos=[10, 10]):
    """
    Draws health bar of a tank on the screen
    :param health_value: health value [0,100]
    :param pos: position of health bar to draw
    :return: none
    """
    color = low_health_color
    if health_value > 65:
        color = good_health_color
    elif health_value > 40:
        color = normal_health_color

    pygame.draw.rect(game_display, color, (pos[0], pos[1], health_value, 25))
    pygame.draw.rect(game_display, white, (pos[0], pos[1], 100, 25), 2)


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

    main_tank_x = int(display_width * 0.9)
    main_tank_y = int(display_height * 0.9)
    main_tank_turret_angle = -pi / 2
    main_tank_power = 50
    move_tank = 0
    angle_change = 0
    power_change = 0

    my_health_bar = 100

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
                    fire_simple_shell(gun, main_tank_turret_angle, main_tank_power)
                elif event.key == pygame.K_z:
                    power_change = 1
                elif event.key == pygame.K_x:
                    power_change = -1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    move_tank = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    angle_change = 0
                elif event.key == pygame.K_z or event.key == pygame.K_x:
                    power_change = 0

        game_display.fill(black)
        gun = draw_tank(main_tank_x, main_tank_y, main_tank_turret_angle, white)
        draw_tank(e_tank_x, e_tank_y, e_turret_angle, white)
        draw_health_bar(my_health_bar, [1490, 10])
        draw_health_bar(e_tank_health)
        show_tanks_power(main_tank_power)

        main_tank_x = update_tank_coordinates(main_tank_x, move_tank)
        main_tank_turret_angle = update_turret_angle(main_tank_turret_angle, angle_change)
        main_tank_power = update_tank_power(main_tank_power, power_change)
        game_display.fill(dark_green, rect=[0, display_height-ground_height, display_width, ground_height])
        pygame.display.update()
        clock.tick(fps)


# game_intro()
game_loop()

pygame.display.update()
halt_whole_game()
