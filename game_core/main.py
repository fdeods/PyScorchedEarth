import pygame
from game_core.game_manager import GameManager
from game_core.constants import players_number, tanks_number

# init game_core and PyGame variables
pygame.init()

manager = GameManager(players_number, tanks_number)
manager.run()

