import pygame
from random import randint
from shapely.geometry import LineString, Point, MultiPoint
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

    def correct_heights(self, interval, new_height):
        for i in range(interval[0], interval[1]):
            self.points[i][1] = new_height

    def update_after_explosion(self, explosion_point, explosion_radius):
        explosion_circle = Point(explosion_point).buffer(explosion_radius).boundary
        max_left = max(0, explosion_point[0]-explosion_radius)
        max_right = min(display_width, explosion_point[0]+explosion_radius)
        for i in range(max_left, max_right):
            ground_line = LineString([[i, display_height], self.points[i]])
            intersection = explosion_circle.intersection(ground_line)
            if isinstance(intersection, MultiPoint):
                first_point = intersection.geoms[0]
                second_point = intersection.geoms[1]
                fst_coordinate = i, min(int(first_point.coords[0][1]), int(second_point.coords[0][1]))
                snd_coordinate = i, max(int(first_point.coords[0][1]), int(second_point.coords[0][1]))

                left_length = fst_coordinate[1] - self.points[i][1]
                self.points[i][1] = snd_coordinate[1] - left_length
            elif isinstance(intersection, Point):
                self.points[i][1] = int(intersection.coords[0][1])
