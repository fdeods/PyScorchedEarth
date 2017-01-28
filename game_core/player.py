from random import randrange
from game_core.constants import display_height, display_width, tank_width, health_bar_length, health_bar_init_positions
from game_core.tank import Tank


class Player:

    def __init__(self, game_display, number_of_tanks, color, player_number):
        self.number_of_tanks = number_of_tanks
        self.color = color
        self.player_number = player_number
        self.health_bars_pos = health_bar_init_positions[player_number]
        self.active_tanks = []
        self.game_display = game_display

    def initialize_tanks(self, actual_tanks_positions):
        """
        Reinitialize available tanks in the game of specified player
        :return: none
        """
        self.active_tanks = []
        initial_y_coord = int(display_height*0.9)
        tab = 5+int(tank_width/2)
        # initialize possible health bar positions
        health_bar_positions = [(self.health_bars_pos[0] + (health_bar_length+10)*i*(-1)**self.player_number,
                                 self.health_bars_pos[1])
                                for i in range(self.number_of_tanks)]
        for i in range(self.number_of_tanks):
            generate = True
            while generate:
                tank_pos_x = randrange(tab, display_width-tab)
                # print(tank_pos_x)
                good_choice = True
                for tank in actual_tanks_positions:
                    if abs(tank_pos_x - tank[0]) < tank_width+10:
                        good_choice = False
                        break
                if good_choice:
                    self.active_tanks.append(
                        Tank(self.game_display, (tank_pos_x, initial_y_coord), health_bar_positions[i], self.color))
                    actual_tanks_positions.append((tank_pos_x, initial_y_coord))
                    generate = False

    def draw_tanks_and_bars(self):
        for tank in self.active_tanks:
            tank.draw_tank()
            tank.draw_health_bar()

    def get_active_tank(self):
        print("Get active tank")
        print(len(self.active_tanks))
        if len(self.active_tanks) == 0:
            return None
        return self.active_tanks[0]

    def update_tanks_list(self):
        """
        Check which tanks are present in the game and delete destroyed ones
        :return: true if player still has tanks, otherwise false
        """
        left_tanks = []
        for tank in self.active_tanks:
            if tank.get_tank_health() == 0:
                tank.self_destruct()
            else:
                left_tanks.append(tank)
        self.active_tanks = left_tanks

