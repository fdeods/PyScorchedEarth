import sys, pygame
from game_core import constants
from libs.pyIgnition import particleEffect, particles
# from game_core import main


class Option:

    hovered = False

    def __init__(self, text, pos, func, font=0):
        """
        Initialize option
        :param text: text to display
        :param pos: initial position of the text
        :param func: function which will be called on mouse onclick event
        :param font: set text font
        """
        self.text = text
        self.pos = pos
        self.func = func
        if (font != 0):
            self.font = font
        else:
            self.font = menu_font
        self.set_rect()
        self.draw()

    def select(self):
        """
        Call function when option is hovered and clicked
        """
        self.func()

    def draw(self):
        """
        Draw text on the screen
        """
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        """
        Set text render options
        """
        self.rend = self.font.render(self.text, True, self.get_color())

    def get_color(self):
        """
        Get hovered and default color of text
        """
        if self.hovered:
            return (251, 223, 124)
        else:
            return (0, 0, 0)


    def set_rect(self):
        """
        Get hovered and default color of text
        """
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.center = (int((constants.display_width / 2)), int(constants.display_height / 2))
        self.rect.top = self.pos


effectLength = 1200
effectTimeTable = ((3030, 3030+effectLength), (7230, 7230+effectLength), (11150, 11150+effectLength), (15250, 15250+effectLength), (19250, 19250+effectLength-200))
effectTimeMin = effectTimeTable[0][0]
effectTimeMax = effectTimeTable[len(effectTimeTable)-1][1]


def isEffect (musicPos):
    if (musicPos < effectTimeMin):
        return False
    if (musicPos > effectTimeMax):
        return True
    for effect in effectTimeTable:
        if (effect[0] <= musicPos <= effect[1]):
            return True
    return False


def emptyFunc ():
    """
    empty function for Option objects
    """
    pass


def drawBlackScreenEffect ():
    filter = pygame.surface.Surface((constants.display_width, constants.display_height))
    filter.fill(pygame.color.Color('White'))
    filter.blit(light, tuple(map(lambda x: x - 50, pygame.mouse.get_pos())))
    screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    pygame.display.flip()

if __name__ == '__main__':
    size = constants.display_width, constants.display_height
    screen = pygame.display.set_mode(size)

    #initialize pictures
    light = pygame.image.load('circle.png')
    bg = pygame.image.load("background.jpg")
    bg = pygame.transform.scale(bg, size)

    #initialize fonts
    pygame.init()
    menu_font = pygame.font.Font('font.ttf', 30)
    title_font = pygame.font.Font('font.ttf', 80)

    #initialize menu options
    first, space = 250, 50
    options = [
        Option("SCORCHED EARTCH", 20, emptyFunc, title_font),
        Option("NEW GAME", (first), emptyFunc),
        Option("OPTIONS", (first + space), emptyFunc),
        Option("EXIT", (first + (space * 2)), sys.exit)
    ]

    #initialize effects
    clock = pygame.time.Clock()
    effect = particleEffect.ParticleEffect(screen, (0, 0), (constants.display_width, constants.display_height))
    gravity = effect.CreatePointGravity(strength = -5, pos = (constants.display_width / 2, constants.display_height / 2 + 100))
    testsource = effect.CreateSource((-10, -10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.5, particlesperframe = 5, particlelife = 75, drawtype = particles.DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)
    testsource.CreateParticleKeyframe(50, colour = (3, 74, 236), length = 10.0)
    testsource.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
    testsource.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
    testsource.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)
    testsource = effect.CreateSource((constants.display_width + 10, 0), initspeed = 5.0, initdirection = 4.15619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.5, particlesperframe = 5, particlelife = 75, drawtype = particles.DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)
    testsource.CreateParticleKeyframe(50, colour = (3, 74, 236), length = 10.0)
    testsource.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
    testsource.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
    testsource.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)

    #initialize music
    pygame.mixer.music.load('backgroundMenuMusic.mp3')
    pygame.mixer.music.play(-1)

    #mainMenu main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(bg, (0, 0))
        effect.Update()
        effect.Redraw()

        #options loop
        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        option.select()
            else:
                option.hovered = False
            option.draw()

        #draw effect
        if (not isEffect(pygame.mixer.music.get_pos())):
            drawBlackScreenEffect()

        pygame.display.update()
