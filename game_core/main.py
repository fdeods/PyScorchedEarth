import pygame
from math import cos, sin, sqrt
from shapely.geometry import LineString
from game_core.constants import *
from game_core.utils import animate_explosion, halt_whole_game
from game_core.tank import Tank

# init game_core and PyGame variables
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ScorchedEarth')
clock = pygame.time.Clock()


# temporary enemy tank
enemy_tank = Tank(game_display, (e_tank_x, e_tank_y), (10, 10), white)


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
    intersection = enemy_tank.check_collision_with_tank(line1)
    if intersection:
        return intersection

    intersection = line1.intersection(line2)

    if intersection:
        return int(intersection.x), int(intersection.y)
    return None


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
            animate_explosion(game_display, collision_point, simple_shell_radius)
            if enemy_tank.apply_damage(collision_point, simple_shell_power, simple_shell_radius):
                print("YOU WON")
            fire = False
        else:
            pygame.draw.circle(game_display, red, (shell_position[0], shell_position[1]), 5)

        pygame.display.update()
        clock.tick(60)


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
        enemy_tank.draw_tank()
        draw_health_bar(my_health_bar, [1490, 10])
        enemy_tank.draw_health_bar()
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
