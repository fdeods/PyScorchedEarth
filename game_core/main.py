import pygame
from math import cos, sin
from shapely.geometry import LineString, Point, MultiPoint
from random import choice
from game_core.constants import *
from game_core.player import Player
from game_core.utils import animate_explosion, halt_whole_game, message_to_screen, animate_ground_sloughing
from game_core.ground import Ground

# init game_core and PyGame variables
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ScorchedEarth')
clock = pygame.time.Clock()

strike_earth_sound = pygame.mixer.Sound("../assets/music/Explosion1.wav")
normal_strike_sound = pygame.mixer.Sound("../assets/music/Explosion2.wav")


# temporary enemy tank
players = []
active_player = None
ground = None


def reinitialize_players():
    """
    Reinitialize available tanks in the game
    :return: none
    """
    global players
    global active_player
    global ground
    ground = Ground(game_display)
    players = []
    left_colors = player_colors[:]
    for i in range(players_number):
        chosen_color = choice(left_colors)
        left_colors.remove(chosen_color)
        players.append(Player(game_display, tanks_number, chosen_color, i))
    init_tanks_positions = []
    for player in players:
        player.initialize_tanks(init_tanks_positions, ground)
    active_player = players[0]


def check_collision(prev_shell_position, current_shell_position):
    """
    Checks collision of shell with other objects and return coordinates of shell collision
    :param prev_shell_position: Coordinates of previous shell position
    :param current_shell_position: Coordinates of updated shell position
    :return: Coordinates of collision or None if no collision detected
    """
    line1 = LineString([prev_shell_position, current_shell_position])

    for player in players:
        intersection = player.check_collision_with_tanks(line1)
        if intersection:
            return intersection

    return ground.check_collision(line1)


def correct_ground(point, explosion_radius):
    left_ground = ground.update_after_explosion(point, explosion_radius)
    if len(left_ground) > 0:
        print("WILL BE SLOUGH")
        draw_all()
        animate_ground_sloughing(game_display, left_ground, ground)
        ground.update_after_sloughing(left_ground)


def apply_players_damages(collision_point, shell_power, shell_radius):
    global players
    explosion_points = []
    for player in players:
        explosion_points.extend(player.apply_damage(collision_point, shell_power, shell_radius))
    if len(explosion_points) > 0:
        for point in explosion_points:
            apply_players_damages(point, tank_explosion_power, tank_explosion_radius)
            correct_ground(point, tank_explosion_radius)


def correct_tanks_heights():
    for player in players:
        player.correct_tanks_heights(ground)


def fire_simple_shell(tank_object):
    """
    Show animation of shooting simple shell
    :param tank_object: tank object that shoots the shell
    :return: none
    """
    (power, gun_angle, fire_sound, color, gun_end_coord) = tank_object.get_init_data_for_shell()
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
        vertical_speed = -((speed * cos(gun_angle)) - 10 * elapsed_time/2)
        horizontal_speed = (speed * sin(gun_angle))
        shell_position[0] += int(horizontal_speed*elapsed_time)
        shell_position[1] += int(vertical_speed*elapsed_time)
        elapsed_time += 0.1

        if shell_position[1] > 2 * display_height:
            break

        collision_point = check_collision(prev_shell_position, shell_position)

        if collision_point:
            animate_explosion(game_display, collision_point, strike_earth_sound, simple_shell_radius)
            correct_ground(collision_point, simple_shell_radius)
            apply_players_damages(collision_point, simple_shell_power, simple_shell_radius)
            correct_tanks_heights()
            fire = False
        else:
            pygame.draw.circle(game_display, color, (shell_position[0], shell_position[1]), 5)

        pygame.display.update()
        clock.tick(60)


def update_players():
    """
    Updates each player information
    :return: none
    """
    global players
    global active_player
    left_players = []
    for player in players:
        if player.is_in_game():
            left_players.append(player)

    if active_player in left_players:
        active_player = left_players[(left_players.index(active_player) + 1) % len(left_players)]
    else:
        if len(left_players) > 0:
            init_index = players.index(active_player)
            while True:
                active_player = players[(init_index+1) % len(players)]
                if active_player in left_players:
                    break

    players = left_players


def draw_all():
    """
    Draws all elements on display
    :return: none
    """
    game_display.fill(black)
    ground.draw()
    for player in players:
        player.draw_tanks_and_bars()


def game_loop():
    global players
    reinitialize_players()
    active_tank = players[0].next_active_tank()
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
                            active_tank = players[0].next_active_tank()
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
                    active_tank = active_player.next_active_tank()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    angle_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    power_change = 0

        draw_all()

        if len(players) <= 1:
            game_over = True

        if active_tank:
            active_tank.show_tank_special()
            active_tank.show_tanks_power()
            active_tank.update_turret_angle(angle_change)
            active_tank.update_tank_power(power_change)

        pygame.display.update()
        clock.tick(fps)


game_loop()
