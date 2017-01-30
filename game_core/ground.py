import pygame
from random import randint
from shapely.geometry import LineString
from game_core.constants import *


class Ground:
    def __init__(self, game_display):
        self.game_display = game_display
        self.ground_height = 0
        self.points = []
        self.reinitialize()

    def reinitialize(self):
        heights = []
        x_step = int(display_width/10)
        for i in range(11):
            heights.append((x_step*i, randint(ground_height_min, ground_height_max)))
        ground_line = LineString(heights)
        for i in range(display_width):
            point = ground_line.intersection(LineString([(i, 0), (i, display_height)]))
            self.points.append([int(point.x), int(point.y)])

        self.ground_height = randint(ground_height_min, ground_height_max)

    def draw(self):
        for i in range(display_width):
            pygame.draw.line(self.game_display,
                             dark_green,
                             (i, display_height),
                             (self.points[i][0], self.points[i][1]))

    def check_collision(self, line):
        intersection_point = None
        step = 1
        if int(line.coords[0][0]) > int(line.coords[1][0]):
            step = -1
        for index in range(int(line.coords[0][0]), int(line.coords[1][0]), step):
            ground_line = LineString([[index, display_height],
                                      [index, self.get_ground_height_at_point(index)]])
            intersection = ground_line.intersection(line)
            if intersection:
                intersection_point = int(intersection.x), int(intersection.y)
                break

        return intersection_point

    def get_ground_height_at_point(self, x_coord):
        if x_coord < 0 or x_coord >= display_width:
            return display_height
        return self.points[x_coord][1]
