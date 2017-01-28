import pygame
import time
from math import cos, sin
from shapely.geometry import LineString
from random import randrange, choice
from game_core.constants import *
from game_core.tank import Tank
from game_core.player import Player
from game_core.utils import animate_explosion, halt_whole_game, message_to_screen

# init game_core and PyGame variables
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ScorchedEarth')
clock = pygame.time.Clock()

strike_earth_sound = pygame.mixer.Sound("../assets/music/Explosion1.wav")
normal_strike_sound = pygame.mixer.Sound("../assets/music/Explosion2.wav")


# temporary enemy tank
players = []


def reinitialize_players():
    """
    Reinitialize available tanks in the game
    :return: none
    """
    init_tanks_positions = []
    for player in players:
        player.initialize_tanks(init_tanks_positions)
    print(init_tanks_positions)


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

    for tank in tanks:
        intersection = tank.check_collision_with_tank(line1)
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
    (power, gun_angle, fire_sound, gun_end_coord) = tank_object.get_init_data_for_shell()
    pygame.mixer.Sound.play(fire_sound)
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
            animate_explosion(game_display, collision_point, strike_earth_sound, simple_shell_radius)
            for tank in tanks:
                tank.apply_damage(collision_point, simple_shell_power, simple_shell_radius)
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


def update_players():
    global players
    left_players = []
    for player in players:
        if player.update_tanks_list():
            left_players.append(player)

    players = left_players


def game_loop():
    global players
    for i in range(players_number):
        players.append(Player(game_display, tanks_number, choice(player_colors), i))
    reinitialize_players()
    active_player = 0
    active_tank = players[0].get_active_tank()
    game_exit = False
    game_over = False
    fps = 15

    angle_change = 0
    power_change = 0

    while not game_exit:
        if game_over:
            message_to_screen(game_display, "Game over", red, -50, FontSize.LARGE, sys_font=False)
            message_to_screen(game_display, "S - play again", green, 50, sys_font=False)
            message_to_screen(game_display, "Q - quit", green, 80, sys_font=False)
            pygame.display.update()
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_exit = True
                            game_over = False
                        if event.key == pygame.K_s:
                            reinitialize_players()
                            game_exit = False
                            game_over = False
                            break
                    elif event.type == pygame.QUIT:
                        game_exit = True
                        game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    power_change = 1
                elif event.key == pygame.K_DOWN:
                    power_change = -1
                elif event.key == pygame.K_LEFT:
                    # change angle
                    angle_change = -angle_step
                elif event.key == pygame.K_RIGHT:
                    # change angle
                    angle_change = angle_step
                elif event.key == pygame.K_SPACE:
                    fire_simple_shell(active_tank)
                    update_players()
                    active_tank = players[(active_player + 1) % len(players)].get_active_tank()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    angle_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    power_change = 0

        game_display.fill(black)
        for player in players:
            player.draw_tanks_and_bars()

        if len(players) == 1:
            game_over = True

        active_tank.show_tanks_power()

        active_tank.update_turret_angle(angle_change)
        active_tank.update_tank_power(power_change)
        game_display.fill(dark_green, rect=[0, display_height-ground_height, display_width, ground_height])
        pygame.display.update()
        clock.tick(fps)

'''
player1 = Player(game_display, 5, red, 0)
player2 = Player(game_display, 5, red, 1)
player3 = Player(game_display, 5, red, 2)
player4 = Player(game_display, 5, red, 3)
tank_poss = []
player1.initialize_tanks(tank_poss)
player2.initialize_tanks(tank_poss)
player3.initialize_tanks(tank_poss)
player4.initialize_tanks(tank_poss)
print(tank_poss)
player1.draw_tanks_and_bars()
player2.draw_tanks_and_bars()
player3.draw_tanks_and_bars()
player4.draw_tanks_and_bars()
'''
game_loop()
