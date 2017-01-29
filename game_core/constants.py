from enum import Enum
from math import pi

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
player_colors = [white, red, green, blue, nice_color]

# tank constants
tank_width = 40
tank_height = 12
turret_width = 3
turret_length = int(tank_width/2) + 5
wheel_width = 5
move_step = 3
angle_step = pi/64
initial_turret_angle = 0 #pi/4
initial_tank_health = 100
tank_explosion_power = 15
tank_explosion_radius = 100

# simple shell constants
min_shell_speed = 12
max_shell_speed = 22
shell_speed_step = (max_shell_speed-min_shell_speed)/100
simple_shell_power = 30
simple_shell_radius = 50

# temporary simple ground
ground_height = 73

# player settings
health_bar_init_positions = [(10, 10), (1490, 10), (10, 45), (1490, 45)]
health_bar_length = 100
players_number = 4
tanks_number = 5


# PyGame fonts
class FontSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
