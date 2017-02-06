import os
import unittest
import pygame
from menu.option import Option
from game_core.tank import Tank
from game_core.constants import *

os.chdir('..')


def empty_function():
    pass


def return_text(text):
    return text


isCalled = False
def called():
    global isCalled
    isCalled = True


class OptionTestCase(unittest.TestCase):

    def test_option_text(self):
        pygame.init()
        title_font = pygame.font.Font('assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, empty_function, title_font)
        self.assertEqual(test.text(), "SCORCHED  EARTH")

    def test_option_text_position(self):
        pygame.init()
        title_font = pygame.font.Font('assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, empty_function, title_font)
        self.assertEqual(test.pos, 20)

    def test_option_hovered(self):
        pygame.init()
        title_font = pygame.font.Font('assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, empty_function, title_font)
        test.hovered = True
        self.assertEqual(test.hovered, True)

    def test_option_hovered_and_color(self):
        pygame.init()
        title_font = pygame.font.Font('assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, empty_function, title_font)
        test.hovered = True
        self.assertEqual(test.get_color(),  (251, 223, 124))
        test.hovered = False
        self.assertEqual(test.get_color(), (0, 0, 0))

    def test_option_select(self):
        global isCalled
        pygame.init()
        title_font = pygame.font.Font('assets/fonts/DeathFromAbove.ttf', 100)
        test = Option(lambda: return_text("SCORCHED  EARTH"), 20, called, title_font)
        isCalled = False
        test.select()
        self.assertEqual(isCalled, True)


class TankTestCase(unittest.TestCase):

    def test_tank_calculate_distance_from_tank_center(self):
        pygame.init()
        tank = Tank((display_height, display_width), (100, 100), (200, 200), black)
        point = tank.calculate_distance_from_tank_center((200, 200))
        self.assertEquals(point, 141)

    def test_tank_turret_and_coordinates(self):
        pygame.init()
        tank = Tank((display_height, display_width), (100, 100), (200, 200), black)
        tac = tank.get_turret_end_coordinates()
        self.assertEquals(tac, (0, 0))

    def test_tank_update_turret_angle(self):
        pygame.init()
        tank = Tank((display_height, display_width), (100, 100), (200, 200), black)
        tank.turret_angle = 0
        self.assertEquals(tank.turret_angle, 0)
        tank.update_turret_angle(50)
        self.assertEquals(tank.turret_angle, 1.5707963267948966)
        tank.turret_angle = 0
        self.assertEquals(tank.turret_angle, 0)
        tank.update_turret_angle(-20)
        self.assertEquals(tank.turret_angle, -1.5707963267948966)

    def test_tank_update_power(self):
        pygame.init()
        tank = Tank((display_height, display_width), (100, 100), (200, 200), black)
        self.assertEquals(tank.tank_power, 50)
        tank.update_tank_power(200)
        self.assertEquals(tank.tank_power, 100)

    def test_tank_get_health(self):
        pygame.init()
        tank = Tank((display_height, display_width), (100, 100), (200, 200), black)
        self.assertEquals(tank.tank_health, 100)
        self.assertEquals(tank.get_tank_health(), 100)

    def test_tank_get_health(self):
        pygame.init()
        tank = Tank((display_height, display_width), (100, 100), (200, 200), black)
        self.assertEquals(tank.position, [100, 100])
        self.assertEquals(tank.get_tank_position(), (100, 100))

    def test_tank_update_position(self):
        pygame.init()
        tank = Tank((display_height, display_width), (100, 100), (200, 200), black)
        self.assertEquals(tank.position, [100, 100])
        tank.update_tank_position((200, 200))
        self.assertEquals(tank.position, [200, 200])


if __name__ == '__main__':
    unittest.main()
