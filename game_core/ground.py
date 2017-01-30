from shapely.geometry import LineString
from game_core.constants import *


class Ground:
    def __init__(self, game_display):
        self.game_display = game_display

    def draw(self):
        self.game_display.fill(dark_green, rect=[0, display_height - ground_height, display_width, ground_height])

    def check_collision(self, line):
        ground_line = LineString([[0, display_height - ground_height], [display_width, display_height - ground_height]])
        intersection = ground_line.intersection(line)

        if intersection:
            return int(intersection.x), int(intersection.y)
        return None
