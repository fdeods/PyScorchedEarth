import pygame
from math import cos, sin
from shapely.geometry import LineString
from game_core.constants import *
from game_core.tank import Tank
from game_core.utils import animate_explosion, halt_whole_game

# init game_core and PyGame variables
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ScorchedEarth')
clock = pygame.time.Clock()


# temporary enemy tank
enemy_tank = Tank(game_display, [e_tank_x, e_tank_y], (10, 10), white)


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


def fire_simple_shell(tank_object):
    """
    Show animation of shooting simple shell
    :param tank_object: tank object that shoots the shell
    :return: none
    """
    (power, gun_angle, gun_end_coord) = tank_object.get_init_data_for_shell()
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

    move_tank = 0
    angle_change = 0
    power_change = 0

    my_tank = Tank(game_display, [int(display_width * 0.9), int(display_height * 0.9)], (1490, 10), white)

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
                    fire_simple_shell(my_tank)
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
        gun = my_tank.draw_tank()
        enemy_tank.draw_tank()
        my_tank.draw_health_bar()
        enemy_tank.draw_health_bar()
        my_tank.show_tanks_power()

        my_tank.update_tank_coordinates(move_tank)
        my_tank.update_turret_angle(angle_change)
        my_tank.update_tank_power(power_change)
        game_display.fill(dark_green, rect=[0, display_height-ground_height, display_width, ground_height])
        pygame.display.update()
        clock.tick(fps)


# game_intro()
game_loop()

pygame.display.update()
halt_whole_game()
