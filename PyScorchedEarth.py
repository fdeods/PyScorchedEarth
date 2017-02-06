import pygame

from game_core.game_manager import GameManager
from game_core.constants import tanks_number, players_number

if __name__ == '__main__':
    pygame.init()
    # MainMenu
    manager = GameManager(players_number, tanks_number)
    manager.run()

