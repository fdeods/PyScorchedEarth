import sys
import pygame
from game_core import constants
from menu.option import Option, GroupedOptions
from libs.pyIgnition import particleEffect, particles
#  from game_core import main

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


def draw_black_screen_effect():
    effect_filter = pygame.surface.Surface((constants.display_width, constants.display_height))
    effect_filter.fill(pygame.color.Color('White'))
    effect_filter.blit(light, tuple(map(lambda x: x - 150, pygame.mouse.get_pos())))
    screen.blit(effect_filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    pygame.display.flip()

if __name__ == '__main__':
    size = constants.display_width, constants.display_height
    screen = pygame.display.set_mode(size)

    # initialize pictures
    light = pygame.image.load('../assets/images/circle.png')
    light = pygame.transform.scale(light, (300, 300))
    bg = pygame.image.load("../assets/images/background.jpg")
    bg = pygame.transform.scale(bg, size)

    # initialize fonts
    pygame.init()
    menu_font = pygame.font.Font('../assets/fonts/font.ttf', 30)
    title_font = pygame.font.Font('../assets/fonts/font.ttf', 80)

    # initialize menu options
    first, space = 250, 50
    mainMenu = GroupedOptions()
    settingsMenu = GroupedOptions()

    mainMenu.add(Option("SCORCHED EARTH", 20, empty_func, title_font))
    mainMenu.add(Option("NEW GAME", first, empty_func, menu_font))
    mainMenu.add(Option("SETTINGS", (first + space), empty_func, menu_font))
    mainMenu.add(Option("EXIT", (first + (space * 2)), sys.exit, menu_font))

    settingsMenu.add(Option("SCORCHED EARTH", 20, empty_func, title_font))
    settingsMenu.add(Option("PLAYERS: X", first, empty_func, menu_font))
    settingsMenu.add(Option("TANKS: X", (first + space), empty_func, menu_font))
    settingsMenu.add(Option("BACK", (first + (space * 2)), empty_func, menu_font))

    displayMenu = mainMenu

    # initialize effects
    clock = pygame.time.Clock()
    effect = particleEffect.ParticleEffect(screen, (0, 0), (constants.display_width, constants.display_height))
    gravity = effect.CreatePointGravity(
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
    pygame.mixer.music.load('../assets/music/backgroundMenuMusic.mp3')
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
