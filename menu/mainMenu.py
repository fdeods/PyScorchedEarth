import sys
import pygame
from game_core import constants
from menu.option import Option, GroupedOptions
from libs.pyIgnition import particleEffect, particles
from game_core.game_manager import GameManager

effect_length = 1200
effectTimeTable = (
    (3030, 3030 + effect_length),
    (7230, 7230 + effect_length),
    (11150, 11150 + effect_length),
    (15250, 15250 + effect_length),
    (19250, 19250 + effect_length - 200)
)
effectTimeMin = effectTimeTable[0][0]
effectTimeMax = effectTimeTable[len(effectTimeTable)-1][1]


def is_effect(music_pos):
    """
    Checks if effect is applicable now
    :param music_pos: position of music
    :return: True/False
    """
    if music_pos < effectTimeMin:
        return False
    if music_pos > effectTimeMax:
        return True
    for effect_value in effectTimeTable:
        if effect_value[0] <= music_pos <= effect_value[1]:
            return True
    return False


def empty_func():
    """
    empty function for Option objects
    """
    pass

pygame.init()
displayMenu = GroupedOptions()
mainMenu = GroupedOptions()
settingsMenu = GroupedOptions()
size = constants.display_width, constants.display_height
screen = pygame.display.set_mode(size)

# initialize pictures
light = pygame.image.load('assets/images/circle.png')
light = pygame.transform.scale(light, (300, 300))
bg = pygame.image.load("assets/images/background.jpg")
bg = pygame.transform.scale(bg, size)


def get_option_text(const, variable=""):
    """
    Returns option text
    :param const: const value
    :param variable: variable value
    :return: const + variable as string
    """
    return const + str(variable)


def go_to_settings():
    """
    Function for Settings button
    :return: none
    """
    global displayMenu
    displayMenu = settingsMenu


def go_to_main_menu():
    """
    Function for Back button
    :return: none
    """
    global displayMenu
    displayMenu = mainMenu


def change_tanks():
    """
    Changes number of tanks in settings
    :return: none
    """
    if constants.tanks_number >= constants.max_tanks_number:
        constants.tanks_number = 1
    else:
        constants.tanks_number += 1


def change_players():
    """
    Changes number of players in settings
    :return: none
    """
    if constants.players_number >= constants. max_players_number:
        constants.players_number = 2
    else:
        constants.players_number += 1


def start_game():
    """
    Function under New Game button
    :return: none
    """
    GameManager(constants.players_number, constants.tanks_number).run()


def draw_black_screen_effect():
    """
    Draw black screen effect
    :return: none
    """
    effect_filter = pygame.surface.Surface((constants.display_width, constants.display_height))
    effect_filter.fill(pygame.color.Color('White'))
    effect_filter.blit(light, tuple(map(lambda x: x - 150, pygame.mouse.get_pos())))
    screen.blit(effect_filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    pygame.display.flip()


def init_menu():
    """
    Initializes menu of the game
    :return: none
    """
    global displayMenu

    # initialize fonts
    menu_font = pygame.font.Font('assets/fonts/DeathFromAbove.ttf', 40)
    title_font = pygame.font.Font('assets/fonts/DeathFromAbove.ttf', 100)

    # initialize menu options
    first, space = 250, 60

    mainMenu.add(Option(lambda: get_option_text("SCORCHED  EARTH"), 20, empty_func, title_font))
    mainMenu.add(Option(lambda: get_option_text("NEW  GAME"), first, start_game, menu_font))
    mainMenu.add(Option(lambda: get_option_text("SETTINGS"), (first + space), go_to_settings, menu_font))
    mainMenu.add(Option(lambda: get_option_text("EXIT"), (first + (space * 2)), sys.exit, menu_font))

    settingsMenu.add(Option(lambda: get_option_text("SCORCHED  EARTH"), 20, empty_func, title_font))
    settingsMenu.add(Option(lambda: get_option_text("PLAYERS  :  ", constants.players_number), first, change_players, menu_font))
    settingsMenu.add(Option(lambda: get_option_text("TANKS  :  ", constants.tanks_number), (first + space), change_tanks, menu_font))
    settingsMenu.add(Option(lambda: get_option_text("BACK"), (first + (space * 2)), go_to_main_menu, menu_font))

    displayMenu = mainMenu

    # initialize effects
    effect = particleEffect.ParticleEffect(screen, (0, 0), (constants.display_width, constants.display_height))
    effect.CreatePointGravity(
        strength=-5,
        pos=(constants.display_width / 2, constants.display_height / 2 + 100)
    )
    testsource = effect.CreateSource(
        (-10, -10),
        initspeed=5.0,
        initdirection=2.35619449,
        initspeedrandrange=2.0,
        initdirectionrandrange=1.5,
        particlesperframe=5,
        particlelife=75,
        drawtype=particles.DRAWTYPE_SCALELINE,
        colour=(255, 255, 255),
        length=10.0
    )
    testsource.CreateParticleKeyframe(50, colour=(3, 74, 236), length=10.0)
    testsource.CreateParticleKeyframe(75, colour=(255, 255, 0), length=10.0)
    testsource.CreateParticleKeyframe(100, colour=(0, 255, 255), length=10.0)
    testsource.CreateParticleKeyframe(125, colour=(0, 0, 0), length=10.0)
    testsource=effect.CreateSource(
        (constants.display_width + 10, 0),
        initspeed=5.0,
        initdirection=4.15619449,
        initspeedrandrange=2.0,
        initdirectionrandrange=1.5,
        particlesperframe=5,
        particlelife=75,
        drawtype=particles.DRAWTYPE_SCALELINE,
        colour=(255, 255, 255),
        length=10.0
    )
    testsource.CreateParticleKeyframe(50, colour=(3, 74, 236), length=10.0)
    testsource.CreateParticleKeyframe(75, colour=(255, 255, 0), length=10.0)
    testsource.CreateParticleKeyframe(100, colour=(0, 255, 255), length=10.0)
    testsource.CreateParticleKeyframe(125, colour=(0, 0, 0), length=10.0)

    # initialize music
    pygame.mixer.music.load('assets/music/backgroundMenuMusic.mp3')
    pygame.mixer.music.play(-1)

    #  mainMenu main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(bg, (0, 0))
        effect.Update()
        effect.Redraw()

        # options loop
        for option in displayMenu.options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                option.set_rend()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        option.select()
            else:
                option.hovered = False
                option.set_rend()
            screen.blit(option.rend, option.rect)

        # draw effect
        if not is_effect(pygame.mixer.music.get_pos()):
            draw_black_screen_effect()

        pygame.display.update()